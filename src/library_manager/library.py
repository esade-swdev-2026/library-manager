from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from library_manager.book_class import Book

LOAN_DAYS = 30


class Library:
    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
        self.books: list[Book] = []
        for row in df.to_dict("records"):
            self.books.append(
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

    def find(self, name: str) -> Book | None:
        for book in self.books:
            if book.name.lower() == name.lower():
                return book
        return None

    def save(self) -> None:
        rows = []
        for book in self.books:
            row = asdict(book)
            row["due_date"] = book.due_date.isoformat() if book.due_date else ""
            rows.append(row)
        pd.DataFrame(rows).to_csv(self.csv_path, index=False)

    def borrow(self, name: str) -> None:
        book = self.find(name)
        if book is None:
            raise ValueError("Book not available")
        if not book.is_available():
            raise ValueError("No existences available")

        book.quantity -= 1
        book.due_date = date.today() + timedelta(days=LOAN_DAYS)
        self.save()

    def return_book(self, name: str) -> bool:
        book = self.find(name)
        if book is None:
            raise ValueError("Book not available")
        if book.due_date is None:
            raise ValueError("This book is not borrowed")

        late = book.is_overdue()
        book.quantity += 1
        book.due_date = None
        self.save()
        return late
