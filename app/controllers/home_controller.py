<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, flash
home_bp = Blueprint("home",__name__)
=======
from flask import Blueprint, render_template, request, redirect, url_for
home_bp = Blueprint('home', __name__)
@home_bp.route('/')
def splash():
    return render_template('splash.html')
@home_bp.route('/index.html')
def index():
    return render_template('index.html')
>>>>>>> 9a170a78507a70e27bfb3891a6193573db7602d0


@home_bp.route("/")
def index():
    return render_template("index.html")