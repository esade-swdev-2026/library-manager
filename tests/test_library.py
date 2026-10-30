from datetime import date

from library_manager.library import Library


def test_find_unexisting_book_returns_none(library: Library) -> None:
    assert library.find("Unexisting Book") is None


def test_find_existing_book_ignores_case(library: Library) -> None:
    book = library.find("Dune")
    assert book is not None
    assert library.find("dUNE") is book


def test_show_due_date_returns_correct_date(library: Library) -> None:
    due_date = library.show_due_date("Emma")
    assert due_date == date(2026, 11, 1)


def test_show_due_date_when_no_due_date_returns_None(library: Library) -> None:
    due_date = library.show_due_date("1984")
    assert due_date is None
