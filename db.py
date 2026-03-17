

from faker import Faker
import sqlite3
import pandas as pd

# Initialize Faker
fake = Faker(['en_IN'])

# Use 'with' to connect to the SQLite database and automatically close the connection when done
with sqlite3.connect('my_database.db') as connection:

    # Create a cursor object
    cursor = connection.cursor()

    delete_query = '''
    DELETE FROM Students
    WHERE name = ?;'''
    student_name = input("Enter the name of the student to delete: ")
    cursor.execute(delete_query, (student_name,))
    connection.commit()

    # update_query = '''
    # UPDATE Students 
    # SET name = ? 
    # WHERE age = ?;
    # '''
    # age = 22
    # student_name = 'John Doe'
    # cursor.execute(update_query, (student_name, age ))
    # connection.commit()



    # select_query = "SELECT * FROM Students;"
    # cursor.execute(select_query)
    # student = cursor.fetchone()
    # three_students = cursor.fetchmany(3)
    # all_students = cursor.fetchall()
    # print(student)
    # print("Three Students:")
    # for student in three_students:
    #     print(student)
    # print("All Students:")
    # print(type(all_students))
    # for student in all_students:
    #     print(student)
    #     print(type(student))



    # df = pd.read_sql_query(select_query, connection)
    # print(df)

    # create_table_query = '''
    # CREATE TABLE IF NOT EXISTS Students (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL,
    #     age INTEGER,
    #     email TEXT
    # );
    # '''
    # cursor.execute('''
    # INSERT INTO Students (name, age, email) 
    # VALUES ('John Doe', 20, 'johndoe@example.com');
    # ''')
    # cursor.execute(create_table_query)


    # insert_query = '''
    # INSERT INTO Students (name, age, email) 
    # VALUES (?, ?, ?);
    # '''
    # students_data = [(fake.name(), fake.random_int(
    #     min=18, max=25), fake.email()) for _ in range(5)]
    # cursor.executemany(insert_query, students_data)
    

    # Commit the changes        SELECT does not need commit, but if you have any INSERT, UPDATE, or DELETE operations, you should commit the changes to save them to the database.
    # connection.commit()

