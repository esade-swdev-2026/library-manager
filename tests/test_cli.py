from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from library_manager import cli
from library_manager.book_class import Book
from library_manager.cli import app
from library_manager.library import find_book, Library

runner = CliRunner()
LOAN_DAYS = 30


@pytest.fixture
def books_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the CLI at a throwaway copy of the catalogue so tests never touch the real one."""
    path = tmp_path / "books.csv"
    path.write_text(
        "name,author,quantity,genre,language,description,due_date\n"
        "1984,George Orwell,1,Dystopian,English,A man rebels against the state.,\n"
        "Dune,Frank Herbert,0,Sci-Fi,English,A noble family fights over a desert planet.,\n"
        "Emma,Jane Austen,0,Romance,English,A young matchmaker meddles in love.,2099-01-01\n"
        "Dracula,Bram Stoker,1,Horror,English,A vampire travels to England.,2000-01-01\n"
    )
    monkeypatch.setattr(cli, "BOOKS_CSV", path)
    return path


def test_borrow_available_book(books_csv: Path) -> None:
    result = runner.invoke(app, ["borrow", "1984"])
    assert result.exit_code == 0
    assert "You have successfully borrowed the book" in result.stdout

    book = pd.read_csv(books_csv).iloc[0]
    assert book["quantity"] == 0
    assert pd.notna(book["due_date"])


def test_borrow_unknown_book_fails(books_csv: Path) -> None:
    result = runner.invoke(app, ["borrow", "Harry Potter"])
    assert result.exit_code == 1
    assert "Book not available" in result.stderr


def test_failed_borrow_leaves_due_date_empty(books_csv: Path) -> None:
    result = runner.invoke(app, ["borrow", "Dune"])
    assert result.exit_code == 1
    assert "No existences available" in result.stderr

    book = pd.read_csv(books_csv).iloc[1]
    assert book["quantity"] == 0
    assert pd.isna(book["due_date"])


def test_return_on_time(books_csv: Path) -> None:
    result = runner.invoke(app, ["return", "Emma"])
    assert result.exit_code == 0
    assert "Thank you for returning the book on time!" in result.stdout

    book = pd.read_csv(books_csv).iloc[2]
    assert book["quantity"] == 1
    assert pd.isna(book["due_date"])


def test_return_late_is_fined(books_csv: Path) -> None:
    result = runner.invoke(app, ["return", "Dracula"])
    assert result.exit_code == 0
    assert "You returned the book late, you will be fined" in result.stdout

    book = pd.read_csv(books_csv).iloc[3]
    assert book["quantity"] == 2
    assert pd.isna(book["due_date"])


def test_return_unknown_book_fails(books_csv: Path) -> None:
    result = runner.invoke(app, ["return", "Harry Potter"])
    assert result.exit_code == 1
    assert "Book not available" in result.stderr


def test_return_book_not_borrowed_fails(books_csv: Path) -> None:
    result = runner.invoke(app, ["return", "1984"])
    assert result.exit_code == 1
    assert "This book is not borrowed" in result.stderr

    book = pd.read_csv(books_csv).iloc[0]
    assert book["quantity"] == 1


def test_find_unexisting_book_returns_none() -> None:
    books = [
        Book("1984", "George Orwell", 1, "Dystopian", "English", "A man rebels.", None),
    ]

    assert find_book(books, "Unexisting Book") is None


def test_find_existing_book_ignores_case() -> None:
    book = Book("Dune", "Frank Herbert", 0, "Sci-Fi", "English", "Desert.", date(2026, 10, 25))

    assert find_book([book], "Dune") is book
    assert find_book([book], "dUNE") is book

def test_borrow_unavailable_book_fails() -> None:
    result = runner.invoke(app, ["borrow", "Unexisting Book"])
    assert result.exit_code == 1
    assert "Book not available" in result.stderr

def test_borrow_book_with_no_stock_fails() -> None:
    library = Library(Path(__file__).parent.parent / "src/library_manager/books-2.csv")
    book = library.books[0]
    book.quantity = 0
    library.save()

    result = runner.invoke(app, ["borrow", book.name])
    assert result.exit_code == 1
    assert "No existences available" in result.stderr

def test_borrow_available_book_decreases_quantity() -> None:
    library = Library(Path(__file__).parent.parent / "src/library_manager/books-2.csv")
    book = library.books[0]
    book.quantity = 1
    library.borrow(book.name)
    assert book.quantity == 0
    
def test_borrow_available_book_creates_correct_due_date() -> None:
    library = Library(Path(__file__).parent.parent / "src/library_manager/books-2.csv")
    book = library.books[0]
    book.quantity = 1
    library.borrow(book.name)
    assert book.due_date == date.today() + timedelta(days=LOAN_DAYS)

def test_return_book_with_None_book_fails() -> None:
    result = runner.invoke(app, ["return", "Unexisting Book"])
    assert result.exit_code == 1
    assert "Book not available" in result.stderr

def test_return_book_with_None_date_fails() -> None:
    library = Library(Path(__file__).parent.parent / "src/library_manager/books-2.csv")
    book = library.books[0]
    book.due_date = None
    library.save()

    result = runner.invoke(app, ["return", book.name])
    assert result.exit_code == 1
    assert "This book is not borrowed" in result.stderr

def test_return_book_overdue_date() -> None:
    library = Library(Path(__file__).parent.parent / "src/library_manager/books-2.csv")
    book = library.books[0]
    book.due_date = date.today() - timedelta(days = 1)
    library.save()

    is_late = library.return_book(book.name)
    assert is_late == True

def test_return_book_correctly_increases_quantity() -> None:
    library = Library(Path(__file__).parent.parent / "src/library_manager/books-2.csv")
    book = library.books[0]
    book.quantity = 1
    book.due_date = date.today()
    library.save()

    library.return_book(book.name)
    assert book.quantity == 2

