# library-manager

A terminal library manager designed for one user. It lets you see the books in the
library, borrow a copy of a book for 30 days and return it, telling you if you returned it
late.

## Install

You need [uv](https://docs.astral.sh/uv/) installed. Then:

```
git clone https://github.com/esade-swdev-2026/library-manager.git
cd library-manager
uv sync
```

This creates a virtual environment and installs everything, including the development
tools, from `uv.lock` — the committed file that pins exact versions so every teammate
and CI resolve the same ones. When you change a dependency in `pyproject.toml`, run
`uv lock` and commit the updated `uv.lock`; CI fails if the two disagree.

## Run

```
uv run library-manager --help
uv run library-manager show
uv run library-manager borrow "Fahrenheit 451"
uv run library-manager return "Fahrenheit 451"
uv run library-manager menu    # interactive: show, borrow and return from one place
```

Book names are not case sensitive. If the book does not exist, has no copies left or was
not borrowed, the program prints a message and exits with code 1.

The books are stored in `src/library_manager/books.csv`, with the columns
`name,author,quantity,genre,language,description,due_date`. `quantity` is the number of
copies left and `due_date` is empty when the book is not borrowed.

## Develop

```
uv run ruff check .          # lint
uv run ruff format .         # format (CI runs `--check` and fails on a diff)
uv run mypy src tests        # types
uv run pytest                # tests
```

These four commands are exactly what `.github/workflows/check.yml` runs on every push.
If they pass here, CI passes. To run all of them at once:

```
./scripts/check.sh
```

## Layout

```
src/library_manager/   the package — importable, installable, not just a script
  cli.py               the typer command-line interface (reads, saves and prints)
  library.py           borrowing and returning rules
  book.py              the Book dataclass
  storage.py           loads and saves the books CSV
  interface.py         formats the books as a table
  books.csv            the library's books
  __main__.py          lets `python -m library_manager` work
scripts/check.sh       runs the four checks
tests/                 pytest tests, mirroring src/
pyproject.toml         dependencies and tool configuration — the single source of truth
```
