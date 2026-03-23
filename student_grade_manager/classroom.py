from student import Student



class Classroom:
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        self.students.append(student)

    def show_students(self):
        for student in self.students:
            print(student)
    
    def remove_student(self, student):
        self.students.remove(student)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
if __name__ == "__main__":
    student1 = Student("John Doe", "12345")
    student1.add_grade(90)
    student1.add_grade(85)
    print(student1)

    classroom = Classroom()
    classroom.add_student(student1)
    classroom.show_students()

    classroom.find_student("12345")