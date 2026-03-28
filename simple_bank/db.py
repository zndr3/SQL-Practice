

from faker import Faker
import sqlite3
from numpy import add
import pandas as pd

# Initialize Faker
fake = Faker(['en_IN'])

# Use 'with' to connect to the SQLite database and automatically close the connection when done
with sqlite3.connect('bank_data.sqlite3') as connection:

    # Create a cursor object
    # cursor = connection.cursor()

    # delete_query = '''
    # DELETE FROM Students
    # WHERE name = ?;'''
    # student_name = input("Enter the name of the student to delete: ")
    # cursor.execute(delete_query, (student_name,))
    # connection.commit()

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

    def delete_row(acc_num):
        # conn = sqlite3.connect('bank_data.sqlite3')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE acc_num = ?;", (acc_num,))
        connection.commit()

    def add_col():
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE transactions ADD COLUMN desc TEXT;")
        connection.commit()


    def insert_data(user_id):
        cursor = connection.cursor()
        cursor.execute('''UPDATE accounts 
                            SET acc_num = 1 
                            WHERE user_id = ?;
                        ''', (user_id,))
        connection.commit()
    
    def get_acc_num(user_id):
        cursor = connection.cursor()
        cursor.execute("SELECT acc_num FROM accounts WHERE user_id=? ORDER BY acc_num DESC", (user_id,))
        print(cursor.fetchone()[0])

    def get_acc_id(user_id, acc_num):
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM accounts WHERE user_id=? AND acc_num=?", (user_id, acc_num))
        print(cursor.fetchone()[0])
        


if __name__ == "__main__":
    delete_row(4)
    # add_col("")
    # get_acc_id("d7499ce3-5fa7-4e29-a97e-d1c5ed8b9b68" , 4)