from flask import Flask
<<<<<<< HEAD

from config import Config
from app.extensions import db, bcrypt, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

        # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # REGISTER BLUEPRINTS
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.attendance_controller import attendance_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
=======
from app.controllers.home_controller import home_bp

def create_app():
    
    app = Flask(__name__)
    app.register_blueprint(home_bp)
>>>>>>> 9a170a78507a70e27bfb3891a6193573db7602d0

    return app