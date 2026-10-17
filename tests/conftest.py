from datetime import date
from pathlib import Path

import pytest

from library_manager import cli
from library_manager.book import Book
from library_manager.library import Library


@pytest.fixture
def today() -> date:
    return date(2026, 10, 14)


@pytest.fixture
def library(today: date) -> Library:
    return Library(
        [
            Book("1984", "George Orwell", 1, "Dystopian", "English", "A man rebels.", None),
            Book("Dune", "Frank Herbert", 0, "Sci-Fi", "English", "A desert planet.", None),
            Book("Emma", "Jane Austen", 0, "Romance", "English", "Matchmaking.", date(2026, 11, 1)),
            Book("Dracula", "Bram Stoker", 1, "Horror", "English", "A vampire.", date(2026, 10, 1)),
            Book("Ulysses", "James Joyce", 0, "Modernist", "English", "A day in Dublin.", today),
        ]
    )


@pytest.fixture
def books_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "books.csv"
    path.write_text(
        "name,author,quantity,genre,language,description,due_date\n"
        "1984,George Orwell,1,Dystopian,English,A man rebels against the state.,\n"
        "Dune,Frank Herbert,0,Sci-Fi,English,A noble family fights over a desert planet.,\n"
        "Emma,Jane Austen,0,Romance,English,A young matchmaker meddles in love.,2099-01-01\n"
        "Dracula,Bram Stoker,1,Horror,English,A vampire travels to England.,2000-01-01\n"
    )
    monkeypatch.setattr(cli, "BOOKS_CSV", path)
    return path
