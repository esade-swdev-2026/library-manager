from library_manager.library import Library


def test_find_unexisting_book_returns_none(library: Library) -> None:
    assert library.find("Unexisting Book") is None


def test_find_existing_book_ignores_case(library: Library) -> None:
    book = library.find("Dune")
    assert book is not None
    assert library.find("dUNE") is book
