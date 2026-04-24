from flask import Flask, render_template, request, redirect, url_for, session
from student import Student
from db import students_col, attendance_col
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

attendance_stack = []  # stack to undo last attendance


# ---------- ADMIN LOGIN ----------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")


# ---------- ADMIN DASHBOARD ----------
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    students = list(students_col.find())
    total_students = len(students)

    # Attendance calculation
    total_attendance = sum(
        attendance_col.count_documents({"roll": s["roll"], "status": "Present"})
        for s in students
    )
    avg_attendance = round((total_attendance / total_students) * 100 if total_students else 0, 2)
    avg_percentage = round(sum([s.get("percentage", 0) for s in students]) / total_students if total_students else 0, 2)

    # Grade distribution
    grade_counts = {"A": 0, "B": 0, "C": 0, "Fail": 0}
    for s in students:
        grade = s.get("grade", "Fail")
        if grade in grade_counts:
            grade_counts[grade] += 1

    return render_template(
        "admin_dashboard.html",
        students=students,
        total_students=total_students,
        avg_attendance=avg_attendance,
        avg_percentage=avg_percentage,
        grade_counts=grade_counts,
        attendance_col=attendance_col
    )


# ---------- LOGOUT ----------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


# ---------- ADD STUDENT ----------
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]

        if students_col.find_one({"roll": roll}):
            return render_template("add_student.html", error="Student already exists")
        students_col.insert_one({
            "roll": roll,
            "name": name,
            "marks": [],
            "total": 0,
            "percentage": 0,
            "grade": "",
            "friends": []
        })
        return redirect(url_for("add_student", success="Student added successfully"))

    return render_template("add_student.html")


# ---------- ENTER MARKS ----------
@app.route("/marks", methods=["GET", "POST"])
def marks():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        roll = request.form["roll"]
        student_data = students_col.find_one({"roll": roll})
        if not student_data:
            return render_template("marks.html", error="Student not found")

        n = int(request.form.get("n_subjects", 0))
        marks_list = []
        for i in range(n):
            mark_value = request.form.get(f"mark{i+1}")
            marks_list.append(int(mark_value) if mark_value else 0)

        s = Student(roll, student_data["name"])
        s.marks = marks_list
        s.calculate_result()

        students_col.update_one(
            {"roll": roll},
            {"$set": {
                "marks": marks_list,
                "total": s.total,
                "percentage": s.percentage,
                "grade": s.grade
            }}
        )
        return redirect(url_for("marks", success="Marks updated successfully"))

    return render_template("marks.html")


# ---------- MARK ATTENDANCE ----------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        roll = request.form["roll"]
        status = request.form["status"]
        date_str = datetime.now().strftime("%Y-%m-%d")

        if attendance_col.find_one({"roll": roll, "date": date_str}):
            return render_template("attendance.html", error="Attendance already marked for today")

        record = {"roll": roll, "status": status, "date": date_str}
        attendance_col.insert_one(record)
        attendance_stack.append(record)
        return redirect(url_for("attendance", success="Attendance marked successfully"))

    return render_template("attendance.html")


# ---------- UNDO ATTENDANCE ----------
@app.route("/undo_attendance")
def undo_attendance():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if not attendance_stack:
        return "No attendance to undo"
    last = attendance_stack.pop()
    attendance_col.delete_one({"roll": last["roll"], "date": last["date"]})
    return redirect(url_for("attendance"))


# ---------- CONNECT STUDENTS ----------
@app.route("/admin/connect", methods=["GET", "POST"])
def connect_students():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    students = list(students_col.find())
    if request.method == "POST":
        roll1 = request.form["roll1"]
        roll2 = request.form["roll2"]
        if roll1 == roll2:
            return render_template("connect_students.html", students=students, error="Cannot connect same student")
        students_col.update_one({"roll": roll1}, {"$addToSet": {"friends": roll2}})
        students_col.update_one({"roll": roll2}, {"$addToSet": {"friends": roll1}})
        return redirect(url_for("connect_students", success="Students connected"))

    return render_template("connect_students.html", students=students)


# ---------- VIEW STUDENT ----------
@app.route("/view_student", methods=["GET", "POST"])
def view_student():
    student = None
    attendance = []
    friends = []

    if request.method == "POST":
        roll = request.form["roll"]
        student = students_col.find_one({"roll": roll})
        if not student:
            return render_template("view_student.html", error="Student not found")

        # Attendance
        attendance = list(attendance_col.find({"roll": roll}))

        # Connections (lookup names using roll numbers)
        friends = []
        for r in student.get("connections", []):
            s = students_col.find_one({"roll": r})
            if s:
                friends.append(s)

    return render_template("view_student.html", student=student, attendance=attendance, friends=friends)

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
