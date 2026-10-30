from library_manager.library import Library


def test_find_unexisting_book_returns_none(library: Library) -> None:
    assert library.find("Unexisting Book") is None


def test_find_existing_book_ignores_case(library: Library) -> None:
    book = library.find("Dune")
    assert book is not None
    assert library.find("dUNE") is book


def test_filter_by_language_returns_matching_books(library: Library) -> None:
    assert len(library.filter_by_language("English")) == 5


def test_filter_by_language_ignores_case(library: Library) -> None:
    assert library.filter_by_language("english") == library.filter_by_language("English")


def test_filter_by_language_returns_empty_for_no_match(library: Library) -> None:
    assert library.filter_by_language("French") == []
