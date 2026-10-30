from datetime import date, timedelta

from library_manager.book import Book

LOAN_DAYS = 30


def find_book(books: list[Book], name: str) -> Book | None:
    for book in books:
        if book.name.lower() == name.lower():
            return book
    return None


def find_book_by_author(books: list[Book], author: str) -> list[Book] | None:
    books_matches = [book for book in books if book.author.lower() == author.lower()]
    return books_matches or None


class Library:
    def __init__(self, books: list[Book]) -> None:
        self.books = books

    def find(self, name: str) -> Book | None:
        return find_book(self.books, name)

    def find_by_author(self, author: str) -> list[Book] | None:
        return find_book_by_author(self.books, author)

    def borrow(self, name: str, today: date) -> None:
        book = self.find(name)
        if book is None:
            raise ValueError("Book not found")
        if not book.is_available():
            raise ValueError("No copies available")

        book.quantity -= 1
        book.due_date = today + timedelta(days=LOAN_DAYS)

    def return_book(self, name: str, today: date) -> bool:
        book = self.find(name)
        if book is None:
            raise ValueError("Book not found")
        if book.due_date is None:
            raise ValueError("This book is not borrowed")

        late = book.is_overdue(today)
        book.quantity += 1
        book.due_date = None
        return late
