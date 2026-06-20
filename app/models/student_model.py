from datetime import datetime, timezone
from app.database.extensions import db


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))


