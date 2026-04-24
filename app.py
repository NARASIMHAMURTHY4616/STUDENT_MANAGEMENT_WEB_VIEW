from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client.student_db
students_col = db.students
attendance_col = db.attendance
admins_col = db.admins

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        admin = admins_col.find_one({"username": username, "password": password})
        if admin:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials","danger")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")
# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    students = list(students_col.find())
    grade_counts = {"A":0, "B":0, "C":0, "Fail":0}

    today_str = str(date.today())
    presents = 0
    absents = 0
    not_marked = 0

    for s in students:
        # Grade counts
        grade = s.get("grade","Fail")
        if grade in grade_counts:
            grade_counts[grade] += 1
        else:
            grade_counts["Fail"] += 1

        # Attendance for today
        att = attendance_col.find_one({"roll": s["roll"], "date": today_str})
        if att:
            if att["status"] == "Present":
                s["today_status"] = "Present"
                presents += 1
            else:
                s["today_status"] = "Absent"
                absents += 1
        else:
            s["today_status"] = "NotMarked"
            not_marked += 1

    total_students = len(students)

    return render_template("admin_dashboard.html",
                           students=students,
                           grade_counts=grade_counts,
                           total_students=total_students,
                           presents=presents,
                           absents=absents,
                           not_marked=not_marked)

# ---------------- ADD STUDENT ----------------
@app.route("/admin/add_student", methods=["GET","POST"])
def add_student():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method=="POST":
        name = request.form["name"]
        roll = request.form["roll"]

        if students_col.find_one({"roll": roll}):
            flash("Student with this roll number already exists!","warning")
            return redirect(url_for("add_student"))

        students_col.insert_one({
            "name": name,
            "roll": roll,
            "marks": [],
            "total": 0,
            "percentage": 0,
            "grade": "",
            "connections": []
        })
        flash("Student added successfully","success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_student.html")

# ---------------- EDIT STUDENT ----------------
@app.route("/admin/edit_student/<roll>", methods=["GET","POST"])
def edit_student(roll):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    student = students_col.find_one({"roll": roll})
    if not student:
        return "Student not found", 404

    if request.method=="POST":
        name = request.form["name"]
        connections = request.form.getlist("connections")
        students_col.update_one({"roll": roll}, {"$set": {"name": name, "connections": connections}})
        flash("Student updated successfully","success")
        return redirect(url_for("admin_dashboard"))

    all_students = list(students_col.find({"roll":{"$ne":roll}}))
    return render_template("edit_student.html", student=student, all_students=all_students)

# ---------------- DELETE STUDENT ----------------
@app.route("/admin/delete_student/<roll>")
def delete_student(roll):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    students_col.delete_one({"roll": roll})
    flash("Student deleted successfully","success")
    return redirect(url_for("admin_dashboard"))

# ---------------- MARKS ----------------
@app.route("/marks/<roll>", methods=["GET","POST"])
def marks(roll):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    student = students_col.find_one({"roll": roll})
    if not student:
        return "Student not found", 404

    if request.method=="POST":
        marks_list = []
        num_subjects = int(request.form.get("num_subjects", 5))
        for i in range(num_subjects):
            mark_key = f"mark{i+1}"
            if mark_key in request.form:
                marks_list.append(int(request.form[mark_key]))

        total = sum(marks_list)
        percentage = total / len(marks_list) if marks_list else 0
        if percentage >= 90: grade = "A"
        elif percentage >= 75: grade = "B"
        elif percentage >= 50: grade = "C"
        else: grade = "Fail"

        students_col.update_one({"roll": roll}, {"$set": {
            "marks": marks_list,
            "total": total,
            "percentage": percentage,
            "grade": grade
        }})
        flash("Marks updated successfully","success")
        return redirect(url_for("admin_dashboard"))

    return render_template("marks.html", student=student)

# ---------------- MARK ATTENDANCE ----------------
@app.route("/mark_attendance", methods=["GET","POST"])
def mark_attendance():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    warning = None
    roll_prefill = request.args.get("roll", "")

    if request.method=="POST":
        roll = request.form.get("roll")
        status = request.form.get("status")
        today_str = str(date.today())

        if not students_col.find_one({"roll": roll}):
            warning = "Student not found"
        elif attendance_col.find_one({"roll": roll, "date": today_str}):
            warning = "Attendance already marked for today!"
        else:
            attendance_col.insert_one({
                "roll": roll,
                "status": status,
                "date": today_str
            })
            flash("Attendance marked successfully","success")
            return redirect(url_for("admin_dashboard"))

    return render_template("attendance.html", warning=warning, roll_prefill=roll_prefill)

# ---------------- VIEW STUDENT ----------------
@app.route("/view_student", methods=["GET","POST"])
def view_student():
    student = None
    attendance = []
    friends = []
    error = None
    if request.method=="POST":
        roll = request.form.get("roll")
        if not roll:
            error = "Please provide a roll number"
        else:
            student = students_col.find_one({"roll": roll})
            if not student:
                error = "Student not found"
            else:
                attendance = list(attendance_col.find({"roll": roll}))
                friends = list(students_col.find({"roll": {"$in": student.get("connections", [])}}))
    return render_template("view_student.html", student=student, attendance=attendance, friends=friends, error=error)

if __name__=="__main__":
    app.run(debug=True)
