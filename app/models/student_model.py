
from app.extensions import db, bcrypt

class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    
    # Secure password field for student access isolated from admins
    password = db.Column(db.String(200), nullable=False)

    # LOWERCASED BACKREF: Connects smoothly to your template files without errors
    attendances = db.relationship(
        "Attendance",
        backref="student_profile",
        lazy=True
    )

    def set_password(self, raw_password):
        """Generates a secure, salted bcrypt hash string for the student."""
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        """Validates incoming raw input against the student's stored hash."""
        return bcrypt.check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<Student {self.name}>"