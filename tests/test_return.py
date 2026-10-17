from datetime import date

import pytest

from library_manager.library import Library


def test_return_on_time(library: Library, today: date) -> None:
    late = library.return_book("Emma", today)

    assert late is False
    book = library.find("Emma")
    assert book is not None
    assert book.quantity == 1
    assert book.due_date is None


def test_return_on_due_date_is_on_time(library: Library, today: date) -> None:
    assert library.return_book("Ulysses", today) is False


def test_return_late(library: Library, today: date) -> None:
    late = library.return_book("Dracula", today)

    assert late is True
    book = library.find("Dracula")
    assert book is not None
    assert book.quantity == 2
    assert book.due_date is None


def test_return_unknown_book_fails(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="Book not found"):
        library.return_book("Harry Potter", today)


def test_return_book_not_borrowed_fails(library: Library, today: date) -> None:
    with pytest.raises(ValueError, match="This book is not borrowed"):
        library.return_book("1984", today)

    book = library.find("1984")
    assert book is not None
    assert book.quantity == 1
