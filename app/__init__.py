from flask import Flask
from config import Config
from app.extensions import db, bcrypt, login_manager

# Note: Global model imports have been removed from here to prevent duplicate mapping errors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # 2. Import and register blueprints inside the factory function scope
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.attendance_controller import attendance_bp
    from app.controllers.dashboard_controller import dashboard_bp
    

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(dashboard_bp)

    # 3. Import model and set up user loader safely nested inside the function
    from app.models.user_model import User
    from app.models.student_model import Student
    from app.models.attendance_model import Attendance
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app