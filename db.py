
from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure

client = MongoClient("mongodb://localhost:27017/")
db = client["student_management"]

students_col = db["students"]
attendance_col = db["attendance"]

# Create unique index safely to prevent duplicate attendance
try:
    attendance_col.create_index(
        [("roll", ASCENDING), ("date", ASCENDING)],
        unique=True
    )
except OperationFailure:
    pass
