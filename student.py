
class Student:
    def __init__(self, roll, name, marks=None):
        self.roll = roll
        self.name = name
        self.marks = marks or []
        self.total = 0
        self.percentage = 0
        self.grade = ""

    def calculate_result(self):
        if not self.marks:
            self.total = 0
            self.percentage = 0
            self.grade = "N/A"
            return

        self.total = sum(self.marks)
        self.percentage = self.total / len(self.marks)

        if self.percentage >= 75:
            self.grade = "A"
        elif self.percentage >= 60:
            self.grade = "B"
        elif self.percentage >= 50:
            self.grade = "C"
        else:
            self.grade = "Fail"
