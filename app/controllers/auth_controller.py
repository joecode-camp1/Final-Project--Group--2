from flask import Blueprint, render_template, session, request, redirect, url_for
import random
import string

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User
from app import db

auth_bp = Blueprint('auth', __name__)


# ======================
# UNIQUE ID GENERATOR
# ======================
def generate_unique_id():
    return "ATT-" + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=7)
    )


# ======================
# SIGNUP ROUTE
# ======================
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    error = None

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'student')  # 🔥 NEW (IMPORTANT)

        # validation
        if not name or not email or not password:
            error = "All fields are required."
            return render_template('auth/signup.html', error=error)

        # check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            error = "Account already exists. Please login instead."
            return render_template('auth/signup.html', error=error)

        # create user
        hashed_password = generate_password_hash(password)
        unique_id = generate_unique_id()

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            unique_id=unique_id,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        # session setup
        session['user_id'] = new_user.id
        session['email'] = new_user.email
        session['role'] = new_user.role
        session['unique_id'] = new_user.unique_id

        # 🔥 ROLE-BASED REDIRECT
        return redirect(url_for('dashboard.dashboard'))


    return render_template('auth/signup.html', error=error)


# ======================
# LOGIN ROUTE
# ======================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            error = "User not found."
            return render_template('auth/login.html', error=error)

        if not check_password_hash(user.password, password):
            error = "Incorrect password."
            return render_template('auth/login.html', error=error)

        # session setup
        session['user_id'] = user.id
        session['email'] = user.email
        session['role'] = user.role
        session['unique_id'] = user.unique_id

        return redirect(url_for('dashboard.dashboard'))


    return render_template('auth/login.html', error=error)


# ======================
# LOGOUT ROUTE
# ======================
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))