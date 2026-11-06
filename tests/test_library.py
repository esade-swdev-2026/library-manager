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


def test_filter_by_language_returns_matching_books(library: Library) -> None:
    assert len(library.filter_by_language("English")) == 6


def test_filter_by_language_ignores_case(library: Library) -> None:
    assert library.filter_by_language("english") == library.filter_by_language("English")


def test_filter_by_language_returns_empty_for_no_match(library: Library) -> None:
    assert library.filter_by_language("French") == []


def test_filter_by_genre_returns_matching_books(library: Library) -> None:
    assert [book.name for book in library.filter_by_genre("Dystopian")] == ["1984"]


def test_filter_by_genre_ignores_case(library: Library) -> None:
    assert library.filter_by_genre("dYSTOPIAN") == library.filter_by_genre("Dystopian")


def test_filter_by_genre_returns_empty_for_no_match(library: Library) -> None:
    assert library.filter_by_genre("Western") == []


def test_show_book_description_ignores_case(library: Library) -> None:
    assert library.show_book_description("dUNE") == "A desert planet."


def test_show_description_of_borrowed_book(library: Library) -> None:
    assert library.show_book_description("Emma") == "Matchmaking."
