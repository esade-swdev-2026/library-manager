from dataclasses import dataclass
import datetime


@dataclass
class Book:
    name: str
    author: str
    quantity: int
    genre: str
    language: str
    description: str
    due_date: datetime.date | None

