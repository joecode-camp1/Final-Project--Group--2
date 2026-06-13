
from os import name

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from app.models.student_model import Student

# Import extensions only
from app.extensions import db, login_manager, bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Local import prevents duplicate tracking errors during application boot
    from app.models.user_model import User 

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.", "warning")
            return redirect(url_for("auth.register"))
            
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Local import safely keeps it scoped to this function runtime
    from app.models.user_model import User 

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard.teacher_dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home.home"))


@auth_bp.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        username = request.form.get('username')
        student_id = request.form.get('student_id')
        course = request.form.get('course')
        password = request.form.get('password')
        
        # Guard clause: Check if student already exists
        existing_student = Student.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash('This Student ID is already registered.', 'danger')
            return redirect(url_for('auth.student_register'))
            
        # 1. Create and stage the new student record
        new_student = Student(
            student_id=student_id,
            name=username,
            course=course,
            password=password # Note: Consider using generate_password_hash(password) for security!
        
        )

        # Salt and hash the password before saving to SQLite
        new_student.set_password(password)

        db.session.add(new_student)
        db.session.commit()
        
        # 2. AUTOMATIC LOGIN: Store identity tracking variables into the session
        session['student_id'] = new_student.student_id
        session['user_name'] = new_student.name
        
        # Send a welcoming flash confirmation
        flash(f'Account created successfully! Welcome to your terminal, {new_student.name}.', 'success')
        
        # 3. REDIRECT: Push them directly onto the student control node dashboard
        return redirect(url_for('dashboard.student_dashboard'))
        
    return render_template('student_register.html')

@auth_bp.route("/student/login", methods=["GET", "POST"])
def student_login():
    from app.models.student_model import Student  # Localized import

    if request.method == "POST":
        student_id = request.form.get("username")  # Pulled from form input field
        password = request.form.get("password")
        
        student = Student.query.filter_by(student_id=student_id).first()
        if student and student.check_password(password):
            
            # Save student session token completely isolated from Admin cookies
            session["student_id"] = student.student_id
            session["student_name"] = student.name
            
            flash(f"Welcome back, {student.name}!", "success")
            return redirect(url_for("dashboard.student_dashboard"))
        else:
            flash("Invalid Student ID or password.", "danger")
        
    return render_template("student_login.html")

@auth_bp.route("/student/logout")
def student_logout():
    # Clear out specific student tokens
    session.pop("student_id", None)
    session.pop("student_name", None)
    flash("You have logged out of the student portal.", "info")
    return redirect(url_for("home.splash"))