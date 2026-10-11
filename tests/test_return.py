from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from library_manager.cli import app

runner = CliRunner()


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
