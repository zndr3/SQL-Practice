
import sqlite3
import hashlib
import os
import base64
import hmac
from database.hash import *
import uuid
import pandas as pd

class InvalidPin(Exception):
    pass

class UserExists(Exception):
    pass

class Bank:
    def __init__(self, db_path="bank_data.sqlite3", ):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
        # self.drop_tables()
        # self.create_users_table()
        # self.create_accounts_table()
        # self.create_transactions_table()

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE `users` (
                               `id` TEXT PRIMARY KEY,
                               `username` TEXT,
                               `password_hash` TEXT);
                                ''')
    def create_accounts_table(self):
        self.cursor.execute('''CREATE TABLE `accounts` (
                                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                                `user_id` TEXT,
                                `acc_type` TEXT,
                                `balance` DECIMAL(19,4),
                                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
                                );
                                ''')
    def create_transactions_table(self):
        self.cursor.execute('''CREATE TABLE `transactions` (
                                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                                `acc_id` INTEGER,
                                `type` TEXT,
                                `amount` DECIMAL(19,4),
                                `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (`acc_id`) REFERENCES `accounts` (`id`)
                                );
                                ''')
        self.conn.commit()
    
    def drop_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS users;")
        self.conn.commit()

    def check_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()
    
    def add_user(self, id, username, password):
        self.cursor.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", (id, username, password))
        self.conn.commit()

    def validate_login(self, name, pin):
        self.cursor.execute("SELECT * FROM users WHERE name=? AND pin=?", (name, pin))
        return self.cursor.fetchone()


    def generate_uuid(self):
        user_id = str(uuid.uuid4())

        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user_id, "jon_doe"))
        conn.commit()

    def check_account(self, user_id):
        self.cursor.execute("SELECT * FROM accounts WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def add_account(self, user_id, acc_type, balance, acc_num):
        self.cursor.execute("INSERT INTO accounts (user_id, acc_type, balance, acc_num) VALUES (?, ?, ?, ?)", (user_id, acc_type, 0.00, acc_num))
        self.conn.commit()
    
    def create_account(self, user_id):
        acc_type = ""
        while acc_type not in ['1', '2']:
            acc_type = input("1. Create Checking Account\n"
                            "2. Create Savings Account\n"
                            "Enter Zero '0' to exit\n"
                            "Enter your choice number: ")
            if acc_type == '0':
                break

            elif acc_type == '1':
                acc_type = "Checking"
                if self.check_account(user_id):
                    acc_num = self.get_acc_num(user_id)[0] + 1
                    self.add_account(user_id, acc_type, 0.00, acc_num)
                    return
                else:
                    acc_num = 1
                    self.add_account(user_id, acc_type, 0.00, acc_num)
                    return
            elif acc_type == '2':
                acc_type = "Savings"
                if self.check_account(user_id):
                    acc_num = self.get_acc_num(user_id)[0] + 1
                    self.add_account(user_id, acc_type, 0.00, acc_num)
                    return
                else:
                    acc_num = 1
                    self.add_account(user_id, acc_type, 0.00, acc_num)
                    return
            else:
                print("Invalid option. Please choose '1' '2' or '0'.")
        
        


    def get_acc_num(self, user_id):
        self.cursor.execute("SELECT acc_num FROM accounts WHERE user_id=? ORDER BY acc_num DESC", (user_id,))
        return self.cursor.fetchone()
        
    def close_acc_num(self, user_id):

        print("Close Account")
        acc_nums = [acc[0] for acc in self.get_acc_nums(user_id)]
        acc_num = 0
        while acc_num not in acc_nums:
            try:
                acc_num = int(input("Enter Zero '0' to exit\nEnter account number to close: "))
                if acc_num == 0:
                    break
                elif acc_num in acc_nums:
                    if not self.get_balance(user_id, acc_num):
                        self.cursor.execute("DELETE FROM accounts WHERE user_id=? AND acc_num=?", (user_id, acc_num))
                        self.conn.commit()
                    else:
                        print("Cannot close account with balance.")
                        print("Please choose another account number.")
                        acc_num = 0
                else:
                    print("No account found with that number.")

            except ValueError:
                print("Invalid input. Please enter a valid account number.")


    def get_balance(self, user_id, acc_num):
        self.cursor.execute("SELECT balance FROM accounts WHERE user_id=? AND acc_num=?", (user_id, acc_num))
        return self.cursor.fetchone()[0]

    
    def get_acc_nums(self, user_id):
        self.cursor.execute("SELECT acc_num FROM accounts WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()
        

    def get_accounts(self, user_id):

        # Separate the query from the data
        query = "SELECT acc_num, acc_type, balance FROM accounts WHERE user_id = ?"
        params = (user_id,)

        # Pass them into read_sql_query separately
        df = pd.read_sql_query(query, self.conn, params=params)

        print(df)
    
    def get_acc_id(self ,user_id, acc_num):
        self.cursor.execute("SELECT id FROM accounts WHERE user_id=? AND acc_num=?", (user_id, acc_num))
        return self.cursor.fetchone()[0]
    
    def deposit(self, acc_id, amount):
        self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, acc_id))
        self.conn.commit()
        self.record_transaction(acc_id, "Deposit", amount, f"Added {amount}")

    def withdraw(self, acc_id, amount):
        self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, acc_id))
        self.conn.commit()
        self.record_transaction(acc_id, "Withdrawal", amount, f"Withdrew {amount}")

    def transfer(self, user_id, acc_num, transfer_to_acc_num, amount):
        self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE user_id = ? AND acc_num = ?", (amount, user_id, acc_num))
        self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ? AND acc_num = ?", (amount, user_id, transfer_to_acc_num))
        self.conn.commit()
        self.record_transaction(self.get_acc_id(user_id, acc_num), "Transfer", amount, f"Account number {acc_num} transferred {amount} to account number {transfer_to_acc_num}")
        
    
    def record_transaction(self, acc_id, type, amount, desc):
        self.cursor.execute("INSERT INTO transactions (acc_id, type, amount, desc) VALUES (?, ?, ?, ?)", (acc_id, type, amount, desc))
        self.conn.commit()

    
    def manage_acc(self, user_id):
        acc_nums = [acc[0] for acc in self.get_acc_nums(user_id)]
        acc_num = 0
        while acc_num not in acc_nums:
            try:
                acc_num = int(input("Enter account number to manage: "))
                if acc_num in acc_nums:
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    choice = 0
                    while choice not in [1, 2, 3]:
                        try:
                            choice = int(input("Enter Zero '0' to exit\nEnter choice number: "))
                            if choice == 0:
                                break
                            elif choice == 1:
                                amount = float(input("Enter amount to deposit: "))
                                self.deposit(self.get_acc_id(user_id, acc_num), amount)
                            
                            elif choice == 2:
                                amount = float(input("Enter amount to withdraw: "))
                                if self.get_balance(user_id, acc_num) < amount:
                                    print("Insufficient funds to withdraw.")
                                else:
                                    self.withdraw(self.get_acc_id(user_id, acc_num), amount)

                            elif choice == 3:
                                transfer_to_acc_num = int(input("Enter account number to transfer to: "))
                                if transfer_to_acc_num not in acc_nums:
                                    print("No account found with that number.")
                                elif transfer_to_acc_num == acc_num:
                                    print("Cannot transfer to the same account.")
                                else:
                                    amount = float(input("Enter amount to transfer: "))
                                    if self.get_balance(user_id, acc_num) < amount:
                                        print("Insufficient funds to transfer.")
                                    else:
                                        self.transfer(user_id, acc_num, transfer_to_acc_num, amount)
                        except ValueError:
                            print("Invalid input. Please enter a valid account number.")
                else:
                    print("No account found with that number.")

            except ValueError:
                print("Invalid input. Please enter a valid account number.")
                

    def dashboard(self, user_id, username):
        # isloggedin = True
        # while isloggedin:
        
        print("Hi " + username + ", Welcome to dashboard!")

        if self.check_account(user_id):
            print("You have an account. Here are your options:")
            self.get_accounts(user_id)
            print("1. Create Account")
            print("2. Close Account")
            print("3. Manage Account")
            print("4. Logout")
            choice = 0

            while choice not in [1, 2, 3, 4]:
                choice = input("Enter choice number: ")
                if choice == '1':
                    self.create_account(user_id)
                    self.dashboard(user_id, username)
                                
                elif choice == '2':
                    self.close_acc_num(user_id)
                    self.dashboard(user_id, username)

                elif choice == '3':
                    self.manage_acc(user_id)
                    self.dashboard(user_id, username)

                elif choice == '4':
                    break
                
                else:
                    print("Invalid option. Please choose '1' '2' '3' or '4'.")
                
        else:
            print("You don't have an account:")
            self.create_account(user_id)
                
        
    def check_password(self, password):
        if len(password) == 6 and password.isdigit():
            return True
        else:
            return False
            
    
    def get_hash(self, username):
        self.cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        hashed_password = self.cursor.fetchone()
        
        return "".join(hashed_password)

    def get_uuid(self, username):
        self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = self.cursor.fetchone()
        
        return "".join(user_id)
    
    def register(self):
        print("Register")
        
        while True:
            username = input("Enter username: ")
            if not self.check_user(username):
                while True:
                    password = input("Enter 6 digit PIN: ")
                    if self.check_password(password):
                        hashed_password = generate_text_hash(password)
                        user_id = str(uuid.uuid4())
                        self.add_user(user_id, username, hashed_password)
                        return
                    else:
                        print("Invalid PIN format. Please enter a 6 digit PIN.")
            else:
                print("User already exists. Please choose a different username.")

    def login(self):
        print("Login")
        username = " "
        while username != "0":
            username = input("Enter Zero '0' to exit\nEnter username: ")
            if username == "0":
                return
            elif self.check_user(username):
                while True:
                    password = input("Enter 6 digit PIN: ")
                    if verify_text_hash(self.get_hash(username), password):
                        self.dashboard(self.get_uuid(username), username)
                        return
                    else:
                        print("Invalid password. Please try again.")
            else:
                print("No user found with that username.")
        
        

def generate_text_hash(password: str):
    """Generates a secure TEXT string for database."""
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
    combined = salt + pw_hash
    
    return base64.b64encode(combined).decode('utf-8')

#stored text from data base hash, provided password from login attempt
def verify_text_hash(stored_text, provided_password):
    """Verify password to the stored TEXT string."""
    combined = base64.b64decode(stored_text)
    salt = combined[:16]
    original_hash = combined[16:]
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 600000)
    
    return hmac.compare_digest(new_hash, original_hash)


if __name__ == "__main__":
    db = Bank()
    while True:   
        print("Welcome to SQL Bank!")
        try:
            enter = input("Do you want to (l)ogin or (r)egister? ").lower()
            if enter == 'l':
                db.login()
            elif enter == 'r':
                db.register()
            else:
                print("Invalid option. Please choose 'l' or 'r'.")

        except UserExists as e:
            print(e)
        except InvalidPin as e:
            print(e)  

        except Exception as e:
            print(e)
        
        