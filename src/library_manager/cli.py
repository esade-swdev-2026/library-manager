from datetime import date
from pathlib import Path

import typer

from library_manager.interface import format_books_table
from library_manager.library import Library
from library_manager.storage import load_books, save_books

app = typer.Typer(help="A terminal library manager.")

# csv: name, author, quantity, genre, language, description, due_date
BOOKS_CSV = Path(__file__).parent / "books.csv"


@app.callback()
def main() -> None:
    """A terminal library manager."""


@app.command()
def borrow(book_name: str) -> None:
    """Borrow a copy of a book."""
    library = Library(load_books(BOOKS_CSV))
    try:
        library.borrow(book_name, date.today())
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    save_books(BOOKS_CSV, library.books)
    typer.echo("You have successfully borrowed the book")


@app.command("return")
def return_book(book_name: str) -> None:
    """Return a borrowed book and tell whether it is late."""
    library = Library(load_books(BOOKS_CSV))
    try:
        late = library.return_book(book_name, date.today())
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    save_books(BOOKS_CSV, library.books)

    if late:
        typer.echo("You returned the book late, you will be fined")
    else:
        typer.echo("Thank you for returning the book on time!")


@app.command("show")
def show() -> None:
    """Show every book in the library."""
    table = format_books_table(load_books(BOOKS_CSV))
    header, *rows = table.splitlines()
    typer.echo(typer.style(header, fg=typer.colors.CYAN, bold=True))
    for row in rows:
        typer.echo(row)


# this just prints the menu, so it has no tests
@app.command("menu")
def menu() -> None:
    while True:
        typer.echo("\n1) Show books\n2) Borrow a book\n3) Return a book\n4) Exit")
        choice = typer.prompt("Choose an option")
        try:
            if choice == "1":
                show()
            elif choice == "2":
                borrow(typer.prompt("Book name"))
            elif choice == "3":
                return_book(typer.prompt("Book name"))
            elif choice == "4":
                typer.echo("Goodbye!")
                break
            else:
                typer.echo("Invalid option, choose 1-4")
        except typer.Exit:
            typer.echo("Please try again.")


if __name__ == "__main__":
    app()
