from datetime import date

import pytest

from library_manager.library import Library


def test_renew_borrowed_book(library: Library, today: date) -> None:
    new_due_date = library.renew("Emma", today)

    assert new_due_date == date(2026, 11, 13)
    book = library.find("Emma")
    assert book is not None
    assert book.due_date == date(2026, 11, 13)
    assert book.quantity == 0


def test_renew_on_due_date_is_allowed(library: Library, today: date) -> None:
    assert library.renew("Ulysses", today) == date(2026, 11, 13)


def test_renew_ignores_case(library: Library, today: date) -> None:
    assert library.renew("eMMA", today) == date(2026, 11, 13)


def test_renew_unknown_book_fails(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="Book not found"):
        library.renew("Harry Potter", today)


def test_renew_book_not_borrowed_fails(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="This book is not borrowed"):
        library.renew("1984", today)


def test_renew_overdue_book_fails(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="Loan is overdue"):
        library.renew("Dracula", today)

    book = library.find("Dracula")
    assert book is not None
    assert book.due_date == date(2026, 10, 1)
