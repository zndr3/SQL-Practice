class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
            print(f'"{self.title}" borrowed successfully.')
        else:
            print(f'"{self.title}" is already borrowed.')

    def return_book(self):
        self.available = True
        print(f'"{self.title}" returned successfully.')

    def display(self):
        status = "Available" if self.available else "Borrowed"
        print(f"{self.title} by {self.author} - {status}")