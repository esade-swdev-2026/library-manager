# We used AI to format the table of the CSV
from dataclasses import asdict

import pandas as pd

from library_manager.book import Book


def format_books_table(books: list[Book]) -> str:
    book_df = (
        pd.DataFrame([asdict(book) for book in books])
        .drop(columns="description")
        .fillna("")
        .astype(str)
    )
    # Left-align every column so long text reads naturally
    formatters = {
        column: f"{{:<{book_df[column].str.len().max()}}}".format for column in book_df.columns
    }
    return book_df.to_string(index=False, justify="left", formatters=formatters)
