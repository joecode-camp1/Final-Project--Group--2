from sqlalchemy.sql import func

from app.extensions import db
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.student_id'), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.now)
    time_out = db.Column(db.DateTime, nullable=True)
    location_before_signin = db.Column(db.String(255), nullable=True)
    is_present = db.Column(db.Boolean, default=True)


     # Core tracking features requested
    time_in = db.Column(db.DateTime, default=datetime.now)
    time_out = db.Column(db.DateTime, nullable=True)
    location_before_signin = db.Column(db.String(255), nullable=True) # Holds Lat/Long strings
    
    def __repr__(self):

        return f"<Attendance {self.student_id}>"