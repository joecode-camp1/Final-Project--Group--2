from flask import Flask
from app.controllers.home_controller import home_bp
from app.controllers.auth_controller import auth_bp


def create_app():
    
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)


    return app