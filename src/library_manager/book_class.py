from dataclasses import dataclass
from datetime import date


@dataclass
class Book:
    name: str
    author: str
    quantity: int
    genre: str
    language: str
    description: str
    due_date: date | None

    def is_available(self) -> bool:
        return self.quantity > 0

    def is_overdue(self) -> bool:
        return self.due_date is not None and date.today() > self.due_date
