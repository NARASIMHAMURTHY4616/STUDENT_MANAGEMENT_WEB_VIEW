# STUDENT_MANAGEMENT_WEB_VIEW
---
---- 
# 📚 Student Attendance & Marks Management System A web-based 
**Student Management System** built using **Flask** and **MongoDB** that allows administrators to manage students, record marks, track attendance, calculate grades, and view student information through an interactive dashboard.

--- 
# 🚀 Features
## 🔐 Admin Authentication 
- Admin login system
-  -Secure session-based authentication
-  - aLogout functionality
 - ## 👨‍🎓 Student Management
   - - Add new students
   - - Edit student details
   - - Delete students
   - - View student profile
 - ## 📊 Marks Management
   - - Add marks for multiple subjects
   - - Automatic calculation of:
      - - Total marks - Percentage
      - - Grade classification
        ### Grade System
| Percentage | Grade |
| ---------- | ----- |
| 90+        | A     |
| 75 – 89    | B     |
| 50 – 74    | C     |
| Below 50   | Fail  |

  ---
         
## 📅 Attendance Management 
 - Mark student attendance
 - Prevent duplicate attendance entries for the same day
 - Attendance status indicators
    -  ### Attendance Badge System
| Badge | Meaning    |
| ----- | ---------- |
| 🟢 P  | Present    |
| 🔴 A  | Absent     |
| ⚪ N   | Not Marked |

    
- Badges are displayed directly on the **student card in the admin dashboard**.

---

# 📈 Admin Dashboard

The dashboard displays:

- Student cards  
- Marks summary  
- Grade badges  
- Attendance status  
- Student connections  

### 📊 Statistics Block

The dashboard also shows:

- Total number of students  
- Students present today  
- Students absent today  
- Grade distribution  

---

# 🔗 Student Connections

Students can have **connections** with other students.

Connections can represent:

- Friends  
- Study partners  
- Team members  

These are visible on the student card.

---

# 🛠 Technologies Used

| Technology | Purpose |
|-----------|--------|
| Python    | Backend programming |
| Flask     | Web framework |
| MongoDB   | Database |
| PyMongo   | MongoDB integration |
| HTML5     | Structure |
| CSS3      | Styling |
| Jinja2    | Flask template engine |

---

# 📁 Project Structure
