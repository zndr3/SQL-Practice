from book import Book

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        print(f'"{title}" added successfully.')

    def show_books(self):
        if not self.books:
            print("No books in library.")
        else:
            for book in self.books:
                book.display()

    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.borrow()
                return
        print("Book not found.")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.return_book()
                return
        print("Book not found.")