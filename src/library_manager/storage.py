from dataclasses import asdict
from datetime import date
from pathlib import Path

import pandas as pd

from library_manager.book import Book


def load_books(csv_path: Path) -> list[Book]:
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    books: list[Book] = []
    for row in df.to_dict("records"):
        books.append(
            Book(
                name=row["name"],
                author=row["author"],
                quantity=int(row["quantity"]),
                genre=row["genre"],
                language=row["language"],
                description=row["description"],
                due_date=date.fromisoformat(row["due_date"]) if row["due_date"] else None,
            )
        )
    return books


def save_books(csv_path: Path, books: list[Book]) -> None:
    rows = []
    for book in books:
        row = asdict(book)
        row["due_date"] = book.due_date.isoformat() if book.due_date else ""
        rows.append(row)
    pd.DataFrame(rows).to_csv(csv_path, index=False)
