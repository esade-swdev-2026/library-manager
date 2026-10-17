from datetime import date

from library_manager.book import Book
from library_manager.interface import format_books_table


def test_table_shows_books_without_description() -> None:
    books = [
        Book("1984", "George Orwell", 0, "Dystopian", "English", "Rebels.", date(2026, 11, 1)),
        Book("Dune", "Frank Herbert", 2, "Sci-Fi", "English", "A desert planet.", None),
    ]

    header, first_row, second_row = format_books_table(books).splitlines()

    assert header.split() == ["name", "author", "quantity", "genre", "language", "due_date"]
    assert "2026-11-01" in first_row
    assert "Frank Herbert" in second_row
    assert "description" not in header
