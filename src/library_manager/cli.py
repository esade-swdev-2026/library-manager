from datetime import date, timedelta
from pathlib import Path

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


if __name__ == "__main__":
    app()
