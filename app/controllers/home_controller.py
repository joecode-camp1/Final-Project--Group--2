from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    # This serves your initial landing or splash page
    return render_template('splash.html')

@home_bp.route('/dashboard')
def dashboard():
    # If you need an index/dashboard route, define it under a distinct path
    return render_template('index.html')