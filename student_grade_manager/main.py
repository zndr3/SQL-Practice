from student import Student
from classroom import Classroom


class OutOfBounds(Exception):
    def __str__(self):
        return "Out of bounds"


classroom = Classroom()

while True:
    try:
        print("1 Add Student\n2 Add Grade\n3 Show Students\n4 Search Student\n5 Remove Student\n6 Exit")
        choice = int(input("Enter choice: "))
        if not 0 < choice < 7:
            raise OutOfBounds
        
        if choice == 1:
            print("Add Student")
            student = Student(name = input("Name: "), student_id = input("Student ID: "))
            classroom.add_student(student)
            # classroom.show_students()
            
        elif choice == 2:
            print("Add Grade")
            student_id = input("Student ID: ")
            for student in classroom.students:
                if student.student_id == student_id:
                    grade = int(input("Grade: "))
                    student.add_grade(grade)

        elif choice == 3:
            print("Show Students")
            classroom.show_students()

        elif choice == 4:
            print("Search Student")
            student_id = input("Student ID: ")
            classroom.find_student(student_id)

        elif choice == 5:
            print("Remove Student")
            student_id = input("Student ID: ")
            classroom.remove_student(student_id)

        elif choice == 6:
            print("Exit")
            break
        
    except OutOfBounds as e:
        print(e)
        continue
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    except Exception as e:
        print(e)