from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from sqlalchemy import func
from app.extensions import db
from app.models.student_model import Student
from app.models.attendance_model import Attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/register", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        name = request.form.get("name")
        student_id = request.form.get("student_id")
        course = request.form.get("course")

        existing_student = Student.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash("Student already exists.", "warning")
            return redirect(url_for("attendance.register_student"))

        new_student = Student(name=name, student_id=student_id, course=course)
        db.session.add(new_student)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for("home.home"))

    return render_template("attendance.html")

@attendance_bp.route("/check-in", methods=["POST"])
def check_in():
    student_id = request.form.get("student_id")
    student = Student.query.filter_by(student_id=student_id).first()

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("attendance.view_attendance"))

    # Block multiple daily records
    today = datetime.now().date()
    existing_attendance = Attendance.query.filter(
        Attendance.student_id == student.id,
        func.date(Attendance.check_in_time) == today
    ).first()

    if existing_attendance:
        flash("You have already checked in today.", "warning")
        return redirect(url_for("attendance.view_attendance"))

    # Parse execution time thresholds
    now = datetime.now()
    status = "Present"
    if now.hour > 8 or (now.hour == 8 and now.minute > 30):
        status = "Late"

    attendance = Attendance(student_id=student.id, status=status)
    db.session.add(attendance)
    db.session.commit()

    flash("Check-in recorded successfully.", "success")
    return redirect(url_for("attendance.view_attendance"))

@attendance_bp.route("/attendance")
def view_attendance():
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Attendance.query.join(Student)

    if search_query:
        query = query.filter(
            Student.name.ilike(f"%{search_query}%") | 
            Student.student_id.ilike(f"%{search_query}%")
        )

    if status_filter:
        query = query.filter(Attendance.status == status_filter)

    # Integrated Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    records = pagination.items

    return render_template("dashboard.html", records=records, pagination=pagination)

@attendance_bp.route("/delete/<int:id>")
def delete_record(id):
    record = Attendance.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash("Attendance record removed.", "info")
    return redirect(url_for("attendance.view_attendance"))