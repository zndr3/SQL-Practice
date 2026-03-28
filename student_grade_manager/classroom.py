from student import Student


class Classroom:
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        self.students.append(student)

    def show_students(self):
        for student in self.students:
            print(student.student_info())
            # print(student.student_info)
    
    def remove_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
        return

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                print(f"{student.name} | {student.student_id}")
                print("Grades: ")
                for grade in student.grades:
                    print(grade, end=" : ")
                print(student.get_average())
        return

        


if __name__ == "__main__":
    student1 = Student("John Doe", "12345")
    student1.add_grade(95)
    student1.add_grade(80)

    student2 = Student("Jane Mar", "45664")
    student2.add_grade(93)
    student2.add_grade(88)

    student3 = Student("Jin Kazama", "34234")
    student3.add_grade(90)
    student3.add_grade(85)
    # print(student1)

    classroom = Classroom()
    classroom.add_student(student1)
    classroom.add_student(student2)
    classroom.add_student(student3)
    print("Show Students: ")
    classroom.show_students()

    print("Find Student: ")
    classroom.find_student("12345")

    classroom.remove_student("12345")
    print("Show Students: ")
    classroom.show_students()