from library import Library

library = Library()

while True:
    print("\n1. Add Book")
    print("2. Show Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        title = input("Book title: ")
        author = input("Author: ")
        library.add_book(title, author)

    elif choice == "2":
        library.show_books()

    elif choice == "3":
        title = input("Book title to borrow: ")
        library.borrow_book(title)

    elif choice == "4":
        title = input("Book title to return: ")
        library.return_book(title)

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")