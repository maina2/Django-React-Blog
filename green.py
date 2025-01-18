import json
import os

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_borrowed": self.is_borrowed
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"], data["isbn"])
        book.is_borrowed = data["is_borrowed"]
        return book


class Library:
    def __init__(self, data_file="library_data.json"):
        self.books = []
        self.data_file = data_file
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]
        self.save_books()

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_borrowed:
                book.is_borrowed = True
                self.save_books()
                return f"Book '{book.title}' has been borrowed."
        return "Book not found or already borrowed."

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.is_borrowed:
                book.is_borrowed = False
                self.save_books()
                return f"Book '{book.title}' has been returned."
        return "Book not found or wasn't borrowed."

    def display_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        print("Available books:")
        for book in self.books:
            status = "Borrowed" if book.is_borrowed else "Available"
            print(f"- {book.title} by {book.author} (ISBN: {book.isbn}) [{status}]")

    def save_books(self):
        with open(self.data_file, "w") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def load_books(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in data]


def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            book = Book(title, author, isbn)
            library.add_book(book)
            print(f"Book '{title}' added to the library.")
        elif choice == "2":
            isbn = input("Enter book ISBN to remove: ")
            library.remove_book(isbn)
            print("Book removed from the library.")
        elif choice == "3":
            isbn = input("Enter book ISBN to borrow: ")
            print(library.borrow_book(isbn))
        elif choice == "4":
            isbn = input("Enter book ISBN to return: ")
            print(library.return_book(isbn))
        elif choice == "5":
            library.display_books()
        elif choice == "6":
            print("Exiting the Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
