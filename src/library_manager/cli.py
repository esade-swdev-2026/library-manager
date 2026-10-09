from datetime import date, timedelta
from pathlib import Path
from library_manager.book_class import Book

import pandas as pd
import typer

app = typer.Typer(help="A terminal library manager.")

# csv: name, author, quantity, genre, language, description, due_date
BOOKS_CSV = Path(__file__).parent / "books-2.csv"


@app.callback()
def main() -> None:
    """A terminal library manager."""


@app.command()
def borrow(book: str) -> None:
    df = pd.read_csv(BOOKS_CSV, dtype={"name": "string", "due_date": "string"})
    match = df["name"].str.lower() == book.lower()

    if not match.any():
        typer.echo("Book not available", err=True)
        raise typer.Exit(code=1)

    if df.loc[match, "quantity"].iloc[0] == 0:
        typer.echo("No existences available", err=True)
        raise typer.Exit(code=1)

    df.loc[match, "quantity"] -= 1
    df.loc[match, "due_date"] = (date.today() + timedelta(days=30)).isoformat()
    df.to_csv(BOOKS_CSV, index=False)
    typer.echo("You have successfully borrowed the book")

def return_book(book: Book) -> None:
    df = pd.read_csv(BOOKS_CSV, dtype={"name": "string", "due_date": "datetime.date"})
    match = df["name"].str.lower() == book.name.lower()

    if not match.any():
            typer.echo("Book not available", err=True)
            raise typer.Exit(code=1)

    is_overdue = date.today() > book.due_date

    if is_overdue:
        typer.echo("You returned the book late, you will be fined")
        df.loc[book.title].quantity += 1
        df.loc[book.title].due_date = None

    else:
        typer.echo("Thank you for returning the book on time!")
        df.loc[book.title].quantity += 1
        df.loc[book.title].due_date = None


if __name__ == "__main__":
    app()
