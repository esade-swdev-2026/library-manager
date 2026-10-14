from datetime import date

import pytest

from library_manager.library import Library


def test_borrow_available_book(library: Library, today: date) -> None:
    library.borrow("1984", today)

    book = library.find("1984")
    assert book is not None
    assert book.quantity == 0
    assert book.due_date == date(2026, 11, 13)


def test_borrow_ignores_case(library: Library, today: date) -> None:
    library.borrow("dracula", today)

    book = library.find("Dracula")
    assert book is not None
    assert book.quantity == 0


def test_borrow_unknown_book_fails(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="Book not available"):
        library.borrow("Harry Potter", today)


def test_failed_borrow_leaves_book_unchanged(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="No existences available"):
        library.borrow("Dune", today)

    book = library.find("Dune")
    assert book is not None
    assert book.quantity == 0
    assert book.due_date is None
