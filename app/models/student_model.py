from app.extensions import db


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    student_id = db.Column(db.String(50), unique=True, nullable=False)

    course = db.Column(db.String(100), nullable=False)

    attendances = db.relationship(
        "Attendance",
        backref="student",
        lazy=True
    )

    def __repr__(self):
        return f"<Student {self.name}>"