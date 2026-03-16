import tkinter as tk
from database.db_manager import DBManager
from ui.login_window import LoginWindow

def main():
    root = tk.Tk()
    db = DBManager()
    app = LoginWindow(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()