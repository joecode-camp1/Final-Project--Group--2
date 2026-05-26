from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from app.extensions import db

from app.models.student_model import Student
from app.models.attendance_model import Attendance

attendance_bp = Blueprint(
    "attendance",
    __name__
)


# REGISTER STUDENT
@attendance_bp.route("/register", methods=["GET", "POST"])
def register_student():

    if request.method == "POST":

        name = request.form.get("name")
        student_id = request.form.get("student_id")
        course = request.form.get("course")

        existing_student = Student.query.filter_by(
            student_id=student_id
        ).first()

        if existing_student:
            return "Student already exists"

        new_student = Student(
            name=name,
            student_id=student_id,
            course=course
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("home.home"))

    return render_template("attendance.html")


# CHECK IN
@attendance_bp.route("/check-in", methods=["POST"])
def check_in():

    student_id = request.form.get("student_id")

    student = Student.query.filter_by(
        student_id=student_id
    ).first()

    if not student:
        return "Student not found"

    attendance = Attendance(
        student_id=student.id
    )

    db.session.add(attendance)
    db.session.commit()

    return redirect(url_for("attendance.view_attendance"))


# VIEW ATTENDANCE
@attendance_bp.route("/attendance")
def view_attendance():

    records = Attendance.query.all()

    return render_template(
        "dashboard.html",
        records=records
    )


# DELETE RECORD
@attendance_bp.route("/delete/<int:id>")
def delete_record(id):

    record = Attendance.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    return redirect(
        url_for("attendance.view_attendance")
    )