from flask import Blueprint
from flask import render_template
from app.extensions import login_manager
from app.models.user_model import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login")
def login():

    return render_template("login.html")