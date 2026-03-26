class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []
    
    def add_grade(self, grade):
        self.grades.append(grade)

    def get_average(self):
        return sum(self.grades) / len(self.grades)

    def student_info(self):
        return f"Name: {self.name} | Student ID: {self.student_id} | Average Grade: {self.get_average()}"
    
    
if __name__ == "__main__":
    student1 = Student("John Doe", "12345")
    student1.add_grade(90)
    student1.add_grade(85)
    print(student1.student_info())
    print(student1.get_average())