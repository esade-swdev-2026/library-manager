from datetime import date, timedelta
from pathlib import Path

from typer.testing import CliRunner

from library_manager.cli import app
from library_manager.library import LOAN_DAYS
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


def test_renew_command_saves_the_new_due_date(books_csv: Path) -> None:
    result = runner.invoke(app, ["renew", "Emma"])
    new_due_date = date.today() + timedelta(days=LOAN_DAYS)
    assert result.exit_code == 0
    assert f"Loan renewed. New due date: {new_due_date.isoformat()}" in result.stdout
    assert load_books(books_csv)[2].due_date == new_due_date


def test_renew_overdue_loan_exits_with_error(books_csv: Path) -> None:
    result = runner.invoke(app, ["renew", "Dracula"])
    assert result.exit_code == 1
    assert "Loan is overdue" in result.stderr


def test_renew_book_not_borrowed_exits_with_error(books_csv: Path) -> None:
    result = runner.invoke(app, ["renew", "1984"])
    assert result.exit_code == 1
    assert "This book is not borrowed" in result.stderr


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


def test_locsv_makes_later_commands_use_the_own_csv(books_csv: Path, tmp_path: Path) -> None:
    own_csv = tmp_path / "own_books.csv"
    own_csv.write_text(books_csv.read_text())

    assert runner.invoke(app, ["locsv", str(own_csv)]).exit_code == 0
    assert runner.invoke(app, ["borrow", "1984"]).exit_code == 0

    assert load_books(own_csv)[0].quantity == 0
    assert load_books(books_csv)[0].quantity == 1


def test_locsv_with_missing_file_exits_with_error_and_keeps_default(
    books_csv: Path, tmp_path: Path
) -> None:
    result = runner.invoke(app, ["locsv", str(tmp_path / "missing.csv")])
    assert result.exit_code == 1

    assert runner.invoke(app, ["borrow", "1984"]).exit_code == 0
    assert load_books(books_csv)[0].quantity == 0
