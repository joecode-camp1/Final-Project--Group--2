
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

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
            return redirect(url_for("home.home"))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home.home"))