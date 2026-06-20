from datetime import datetime, timedelta, timezone
from collections import defaultdict
import json

from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify

from app.models import AttendanceRecord, AttendanceSession, User
from app import db

dashboard_bp = Blueprint('dashboard', __name__)


# =========================================================
# TIME HELPERS
# =========================================================

def _now():
    return datetime.now(timezone.utc)


def _time_ago(dt):
    if not dt:
        return ""

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = _now() - dt

    if delta < timedelta(minutes=1):
        return "Just now"
    if delta < timedelta(hours=1):
        mins = int(delta.total_seconds() // 60)
        return f"{mins} min ago"
    if delta < timedelta(days=1):
        hrs = int(delta.total_seconds() // 3600)
        return f"{hrs} hr ago"
    if delta < timedelta(days=2):
        return "Yesterday"

    return dt.strftime("%b %d")


# =========================================================
# REAL-TIME CHART BUILDER (DAY/WEEK/MONTH READY)
# =========================================================

def _build_chart_data(records, mode="week"):
    today = _now().date()

    if mode == "day":
        days = 1
    elif mode == "month":
        days = 30
    else:
        days = 7

    date_range = [today - timedelta(days=i) for i in range(days - 1, -1, -1)]

    stats = defaultdict(lambda: {"present": 0, "total": 0})

    for r in records:
        if not getattr(r, "created_at", None):
            continue

        d = r.created_at.date()

        if d in date_range:
            stats[d]["total"] += 1
            if r.status == "present":
                stats[d]["present"] += 1

    labels = []
    values = []

    for d in date_range:
        labels.append(d.strftime("%a") if mode != "month" else d.strftime("%d"))
        bucket = stats[d]

        if bucket["total"] == 0:
            values.append(0)
        else:
            values.append(round(bucket["present"] / bucket["total"] * 100))

    return {
        "labels": labels,
        "values": values
    }


# =========================================================
# CORE DASHBOARD ROUTE
# =========================================================

@dashboard_bp.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    role = session.get('role', 'student')
    user_id = session.get('user_id')

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    # -------------------------
    # RECORDS (OPTIMIZED)
    # -------------------------
    if role == "student":
        records = AttendanceRecord.query.filter_by(student_id=user_id).all()
        template = "dashboard/student_dashboard.html"
    else:
        records = AttendanceRecord.query.all()
        template = "dashboard/admin_teacher_dashboard.html"

    # -------------------------
    # STATS
    # -------------------------
    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    absent = sum(1 for r in records if r.status == "absent")

    attendance_rate = round((present / total) * 100, 2) if total else 0

    # -------------------------
    # DEFAULT MODE = WEEK
    # -------------------------
    chart_data = _build_chart_data(records, mode="week")

    # -------------------------
    # ADMIN ONLY FEATURES
    # -------------------------
    notifications = []
    recent_activity = []
    active_classes_count = 0
    late_arrivals_count = 0

    if role != "student":

        # ACTIVE CLASSES TODAY
        active_classes_count = db.session.query(AttendanceSession.class_id)\
            .filter(AttendanceSession.date == _now().date())\
            .distinct().count()

        # LATE ARRIVALS
        for r in records:
            if not getattr(r, "session", None):
                continue

            if not (r.sign_in_time and r.session.start_time):
                continue

            scheduled = datetime.combine(
                r.session.date,
                r.session.start_time
            ).replace(tzinfo=timezone.utc)

            sign_in = r.sign_in_time
            if sign_in.tzinfo is None:
                sign_in = sign_in.replace(tzinfo=timezone.utc)

            if (sign_in - scheduled) > timedelta(minutes=10):
                late_arrivals_count += 1

        # RECENT ACTIVITY
        recent_activity = []
        for r in sorted(records, key=lambda x: x.created_at or _now(), reverse=True)[:6]:

            status = "positive" if r.status == "present" else "negative"

            recent_activity.append({
                "status": status,
                "text": f"{r.student_name} marked {r.status}",
                "time_ago": _time_ago(r.created_at)
            })

        # SIMPLE NOTIFICATION EXAMPLE
        if absent > 0:
            notifications.append({
                "type": "danger",
                "title": f"{absent} absences recorded",
                "subtitle": "Check attendance logs",
                "time": "Today"
            })

    # -------------------------
    # FINAL RESPONSE
    # -------------------------
    return render_template(
        template,
        user=user,
        role=role,

        total_records=total,
        present_count=present,
        absent_count=absent,
        attendance_rate=attendance_rate,

        chart_data=chart_data,
        chart_js=json.dumps(chart_data),

        notifications=notifications,
        notification_count=len(notifications),
        recent_activity=recent_activity,

        active_classes_count=active_classes_count,
        late_arrivals_count=late_arrivals_count,

        active_page="dashboard",
        current_year=_now().year
    )


# =========================================================
# 🔥 REAL-TIME API ENDPOINT (IMPORTANT ADDITION)
# =========================================================

@dashboard_bp.route('/dashboard/data')
def dashboard_data():

    if 'user_id' not in session:
        return jsonify({"error": "unauthorized"}), 401

    mode = request.args.get("mode", "week")
    user_id = session.get("user_id")
    role = session.get("role", "student")

    if role == "student":
        records = AttendanceRecord.query.filter_by(student_id=user_id).all()
    else:
        records = AttendanceRecord.query.all()

    chart = _build_chart_data(records, mode)

    return jsonify({
        "chart": chart,
        "total": len(records),
        "present": sum(1 for r in records if r.status == "present"),
        "absent": sum(1 for r in records if r.status == "absent"),
    })


# =========================================================
# SEARCH (UNCHANGED BUT CLEANED)
# =========================================================

@dashboard_bp.route('/search')
def search():

    query = request.args.get('query', '').strip()

    if not query:
        return jsonify({"results": []})

    users = User.query.filter(User.name.ilike(f"%{query}%")).limit(5).all()

    records = AttendanceRecord.query.filter(
        AttendanceRecord.student_name.ilike(f"%{query}%")
    ).limit(5).all()

    return jsonify({
        "results": [
            *[
                {
                    "type": "user",
                    "label": f"{u.name} · {u.role}",
                    "href": url_for('dashboard.dashboard')
                } for u in users
            ],
            *[
                {
                    "type": "attendance",
                    "label": f"{r.student_name} — {r.status}",
                    "href": url_for('dashboard.dashboard')
                } for r in records
            ]
        ]
    })
@dashboard_bp.route('/attendance_percentage')
def attendance_percentage():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template(
        "dashboard/attendance_percentage.html",
        active_page="attendance_percentage"
    )
@dashboard_bp.route('/dashboard/classes-created')
def classes_created():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    sessions = AttendanceSession.query.order_by(AttendanceSession.created_at.desc()).all()

    return render_template(
        "dashboard/classes_created.html",
        sessions=sessions,
        active_page="classes"
    )
@dashboard_bp.route('/dashboard/students-registered')
def students_registered():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    students = User.query.filter_by(role="student").all()

    return render_template(
        "dashboard/students_registered.html",
        students=students,
        active_page="students"
    )
@dashboard_bp.route('/dashboard/live-notifications')
def live_notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    records = AttendanceRecord.query.order_by(AttendanceRecord.created_at.desc()).limit(20).all()

    alerts = []

    for r in records:
        if r.status == "absent":
            alerts.append({
                "type": "danger",
                "text": f"{r.student_name} was absent",
                "time": r.created_at
            })

    return render_template(
        "dashboard/live_notifications.html",
        alerts=alerts,
        active_page="alerts"
    )

@dashboard_bp.route('/start-session')
def start_session():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template(
        "dashboard/start_session.html",
        active_page="start"
    )
@dashboard_bp.route('/mark-attendance')
def mark_attendance():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template(
        "dashboard/mark_attendance.html",
        active_page="mark_attendance"
    )