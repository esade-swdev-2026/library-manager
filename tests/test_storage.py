from datetime import date
from pathlib import Path

from library_manager.storage import load_books, save_books


def test_load_books_reads_every_row(books_csv: Path) -> None:
    books = load_books(books_csv)

    assert [book.name for book in books] == ["1984", "Dune", "Emma", "Dracula"]
    assert books[0].quantity == 1
    assert books[0].due_date is None
    assert books[2].due_date == date(2099, 1, 1)


def test_saved_books_load_back_unchanged(books_csv: Path) -> None:
    books = load_books(books_csv)
    books[0].quantity = 0
    books[0].due_date = date(2026, 11, 13)

    save_books(books_csv, books)

    assert load_books(books_csv) == books
