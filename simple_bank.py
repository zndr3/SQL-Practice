import sqlite3
import hashlib
import os
import base64
import hmac
from database.hash import *
import uuid

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
    
    def create_account(self, user_id, acc_type):
        self.cursor.execute("INSERT INTO accounts (user_id, acc_type, balance) VALUES (?, ?, ?)", (user_id, acc_type, 0.00))
        self.conn.commit()

    def dashboard(self, user_id):
        print("Welcome to dashboard!")

        if self.check_account(user_id):
            print("You have an account. Here are your options:")
            print("1. View Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Logout")
        else:
            print("You don't have an account:")
            acc_type = input("1. Create Checking Account, enter (c)\n"
                             "2. Create Savings Account, enter (s)\n"
                             "Enter your choice: ").lower()
            if acc_type == 'c':
                self.create_account(user_id, "Checking")
            elif acc_type == 's':
                self.create_account(user_id, "Savings")
            else:
                print("Invalid option. Please choose 'c' or 's'.")
            self.dashboard(user_id)
            
    
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
        username = input("Enter username: ")
        password = input("Enter 6 digit PIN: ")

        if not self.check_user(username):
            if self.check_password(password):
                hashed_password = generate_text_hash(password)
                user_id = str(uuid.uuid4())
                self.add_user(user_id, username, hashed_password)
                return
            else:
                print("Invalid PIN format. Please enter a 6 digit PIN.")
                self.register()
        else:
            print("User already exists. Please choose a different username.")
            self.register()

    def login(self):
        print("Login")
        try:
            username = input("Enter username: ")
            password = input("Enter 6 digit PIN: ")
            
            if self.check_user(username):
                if verify_text_hash(self.get_hash(username), password):
                    self.dashboard(self.get_uuid(username))
                else:
                    print("Invalid password. Please try again.")
            else:
                print("No user found with that username.")
                print("Redirecting to registration...")
                self.register()

        except UserExists as e:
            print(e)
        except InvalidPin as e:
            print(e)  
        
        

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
        print("Nothing for now")
        
        