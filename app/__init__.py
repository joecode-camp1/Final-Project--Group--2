from flask import Flask
from app.config import Config
from app.database.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()

    return app