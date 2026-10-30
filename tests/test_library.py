import pytest

from library_manager.library import Library


def test_find_unexisting_book_returns_none(library: Library) -> None:
    assert library.find("Unexisting Book") is None


def test_find_existing_book_ignores_case(library: Library) -> None:
    book = library.find("Dune")
    assert book is not None
    assert library.find("dUNE") is book


@pytest.mark.parametrize(
    ("author", "expected_names"),
    [
        ("George Orwell", ["1984", "Animal Farm"]),
        ("george orwell", ["1984", "Animal Farm"]),
        ("Jane Austen", ["Emma"]),
        ("Unknown Author", []),
    ],
)
def test_find_by_author(library: Library, author: str, expected_names: list[str]) -> None:
    books = library.find_by_author(author) or []
    assert [book.name for book in books] == expected_names
