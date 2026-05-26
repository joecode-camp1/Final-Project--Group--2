from datetime import datetime

from app.extensions import db


class Attendance(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    check_in_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="Present"
    )

    def __repr__(self):
        return f"<Attendance {self.student_id}>"