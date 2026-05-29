from app.extensions import db, bcrypt
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="admin")


    def set_password(self, password):
        # Generates a secure, salted bcrypt hash string
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Validates incoming raw input against the hash string
        return bcrypt.check_password_hash(self.password_hash, password)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="admin"
    )