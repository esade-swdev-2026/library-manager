from pathlib import Path

import pytest

from library_manager import cli


@pytest.fixture
def books_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the CLI at a throwaway copy of the catalogue so tests never touch the real one."""
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
