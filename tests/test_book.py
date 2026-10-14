from datetime import date

from library_manager.book_class import Book


def make_book(quantity: int, due_date: date | None) -> Book:
    return Book("1984", "George Orwell", quantity, "Dystopian", "English", "", due_date)


def test_book_with_copies_is_available() -> None:
    assert make_book(quantity=1, due_date=None).is_available()


def test_book_without_copies_is_not_available() -> None:
    assert not make_book(quantity=0, due_date=None).is_available()


def test_book_without_due_date_is_not_overdue(today: date) -> None:
    assert not make_book(quantity=1, due_date=None).is_overdue(today)


def test_book_due_today_is_not_overdue(today: date) -> None:
    assert not make_book(quantity=0, due_date=today).is_overdue(today)


def test_book_due_yesterday_is_overdue(today: date) -> None:
    assert make_book(quantity=0, due_date=date(2026, 10, 13)).is_overdue(today)


def test_book_due_tomorrow_is_not_overdue(today: date) -> None:
    assert not make_book(quantity=0, due_date=date(2026, 10, 15)).is_overdue(today)
