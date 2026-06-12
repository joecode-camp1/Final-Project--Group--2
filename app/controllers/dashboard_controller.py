
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.student_model import Student
from app.models.attendance_model import Attendance
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('auth.student_login'))
    
    student = Student.query.filter_by(student_id=session['student_id']).first()
    
    # Feature 1: Load personal history log data array
    history = Attendance.query.filter_by(student_id=student.student_id).order_by(Attendance.time_in.desc()).all()
    
    # Feature 2: Detect if they have an active open check-in running right now
    active_log = Attendance.query.filter_by(student_id=student.student_id, time_out=None).first()
    is_signed_in = True if active_log else False
    
    return render_template('student_dashboard.html', student=student, history=history, is_signed_in=is_signed_in)

@dashboard_bp.route('/student/signin', methods=['POST'])
def student_sign_in():
    if 'student_id' not in session:
        return redirect(url_for('auth.student_login'))
    
    student_id = session['student_id']
    location = request.form.get('location', 'Unknown')

    active_log = Attendance.query.filter_by(student_id=student_id, time_out=None).first()
    if active_log:
        flash('You are already tracking inside an open class room node.', 'danger')
        return redirect(url_for('dashboard.student_dashboard'))

    new_log = Attendance(
        student_id=student_id,
        location_before_signin=location,
        time_in=datetime.now()
    )
    db.session.add(new_log)
    db.session.commit()
    
    flash('Sign-in record compiled successfully.', 'success')
    return redirect(url_for('dashboard.student_dashboard'))

@dashboard_bp.route('/student/signout', methods=['POST'])
def student_sign_out():
    if 'student_id' not in session:
        return redirect(url_for('auth.student_login'))

    student_id = session['student_id']
    active_log = Attendance.query.filter_by(student_id=student_id, time_out=None).first()

    if not active_log:
        flash('No active sign-in record state was discovered.', 'danger')
        return redirect(url_for('dashboard.student_dashboard'))

    active_log.time_out = datetime.now()
    db.session.commit()

    flash('Sign-out track index updated.', 'success')
    return redirect(url_for('dashboard.student_dashboard'))

@dashboard_bp.route('/teacher/dashboard')
def teacher_dashboard():
    all_records = Attendance.query.order_by(Attendance.time_in.desc()).all()
    
    # Feature 3: Calculate global system telemetry indicators for metrics display
    active_count = Attendance.query.filter_by(time_out=None).count()
    
    # Filter count checking for profiles that manually bypassed or blocked tracking hardware interfaces
    flagged_count = Attendance.query.filter(
        (Attendance.location_before_signin == 'Location Denied') | 
        (Attendance.location_before_signin == 'Unknown')
    ).count()

    return render_template(
        'teacher_dashboard.html', 
        active_logs=all_records, 
        active_count=active_count, 
        flagged_count=flagged_count
    )