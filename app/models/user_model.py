from app.extensions import db, bcrypt
from flask_login import UserMixin 

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, raw_password):
        """Generates a secure hash string for administrative accounts."""
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        """Validates administrative log-in keys."""
        return bcrypt.check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<Admin User {self.username}>"