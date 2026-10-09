from pathlib import Path

import typer

from library_manager.library import Library

app = typer.Typer(help="A terminal library manager.")

# csv: name, author, quantity, genre, language, description, due_date
BOOKS_CSV = Path(__file__).parent / "books-2.csv"


@app.callback()
def main() -> None:
    """A terminal library manager."""


@app.command()
def borrow(book: str) -> None:
    library = Library(BOOKS_CSV)
    try:
        library.borrow(book)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo("You have successfully borrowed the book")


@app.command("return")
def return_book(book: str) -> None:
    library = Library(BOOKS_CSV)
    try:
        late = library.return_book(book)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error

    if late:
        typer.echo("You returned the book late, you will be fined")
    else:
        typer.echo("Thank you for returning the book on time!")


if __name__ == "__main__":
    app()
