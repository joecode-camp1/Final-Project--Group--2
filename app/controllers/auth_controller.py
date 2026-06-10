from flask import Blueprint, render_template
from flask import request, redirect, url_for
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        print(email, username, password)  # test if form is working

        return redirect(url_for('home.index'))

    return render_template("login.html")
