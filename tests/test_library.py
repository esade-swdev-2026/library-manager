from pathlib import Path

from library_manager.library import Library


def test_find_unexisting_book_returns_none(books_csv: Path) -> None:
    library = Library(books_csv)
    assert library.find("Unexisting Book") is None


def test_find_existing_book_ignores_case(books_csv: Path) -> None:
    library = Library(books_csv)
    book = library.find("Dune")
    assert book is not None
    assert library.find("dUNE") is book
