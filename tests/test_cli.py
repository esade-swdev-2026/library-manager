from pathlib import Path

from typer.testing import CliRunner

from library_manager.cli import app
from library_manager.storage import load_books

runner = CliRunner()


def test_borrow_command_saves_the_loan(books_csv: Path) -> None:
    result = runner.invoke(app, ["borrow", "1984"])
    assert result.exit_code == 0
    assert "You have successfully borrowed the book" in result.stdout
    assert load_books(books_csv)[0].quantity == 0


def test_return_command_saves_the_return(books_csv: Path) -> None:
    result = runner.invoke(app, ["return", "Dracula"])
    assert result.exit_code == 0
    assert "You returned the book late, you will be fined" in result.stdout
    assert load_books(books_csv)[3].quantity == 2


def test_bad_input_exits_with_error(books_csv: Path) -> None:
    result = runner.invoke(app, ["borrow", "Harry Potter"])
    assert result.exit_code == 1
    assert "Book not found" in result.stderr


def test_filter_command_lists_matching_books(books_csv: Path) -> None:
    result = runner.invoke(app, ["filter", "English"])
    assert result.exit_code == 0
    assert "1984" in result.stdout


def test_filter_command_with_no_matches_exits_with_error(books_csv: Path) -> None:
    result = runner.invoke(app, ["filter", "French"])
    assert result.exit_code == 1
    assert "No books found" in result.stdout
