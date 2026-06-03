
from flask import Blueprint, render_template, request, redirect, url_for, flash
home_bp = Blueprint("home",__name__)

from flask import Blueprint, render_template, request, redirect, url_for
home_bp = Blueprint('home', __name__)
@home_bp.route('/')
def splash():
    return render_template('splash.html')
@home_bp.route('/index.html')
def index():
    return render_template('index.html')



@home_bp.route("/")
def index():
    return render_template("index.html")