from datetime import date, timedelta

from library_manager.book_class import Book

LOAN_DAYS = 30


def find_book(books: list[Book], name: str) -> Book | None:
    for book in books:
        if book.name.lower() == name.lower():
            return book
    return None


class Library:
    def __init__(self, books: list[Book]) -> None:
        self.books = books

    def find(self, name: str) -> Book | None:
        return find_book(self.books, name)

    def borrow(self, name: str, today: date) -> None:
        book = self.find(name)
        if book is None:
            raise ValueError("Book not available")
        if not book.is_available():
            raise ValueError("No existences available")

        book.quantity -= 1
        book.due_date = today + timedelta(days=LOAN_DAYS)

    def return_book(self, name: str, today: date) -> bool:
        book = self.find(name)
        if book is None:
            raise ValueError("Book not available")
        if book.due_date is None:
            raise ValueError("This book is not borrowed")

        late = book.is_overdue(today)
        book.quantity += 1
        book.due_date = None
        return late
