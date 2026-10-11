from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from library_manager.cli import app

runner = CliRunner()


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