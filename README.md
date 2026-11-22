# library-manager

A terminal library manager designed for one user. It lets you see the books in the
library, borrow a copy of a book for 30 days, renew the loan before it is due and return it,
telling you if you returned it late.

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
uv run library-manager renew "Fahrenheit 451"     # due 30 days from today, only before the due date
uv run library-manager return "Fahrenheit 451"
uv run library-manager filter Spanish             # books in a language
uv run library-manager gfilter "Science Fiction"  # books of a genre
uv run library-manager afilter "Jane Austen"      # books by an author
uv run library-manager description "Dune"         # what a book is about
uv run library-manager menu    # interactive: every command above from one place
uv run library-manager locsv my_books.csv         # use your own books csv from now on
```

Book names, languages, genres and authors are not case sensitive. If the book does not
exist, has no copies left, was not borrowed or is overdue when renewing, or a filter finds
no books, the program prints a message and exits with code 1. The same happens if the csv
saved with `locsv` no longer exists or is missing a column.

The books are stored in `data/example_books.csv`, with the columns
`name,author,quantity,genre,language,description,due_date`. `quantity` is the number of
copies left and `due_date` is empty when the book is not borrowed.

To use your own books instead, run `locsv` with the path to a csv that has the same
columns. The path is saved in `~/.library_manager`, so every later command uses that csv;
delete that file to go back to the example books. To save it somewhere else, set the
`LIBRARY_MANAGER_CONFIG` environment variable to the file you want to use (the Docker
image sets it to `/app/data/.library_manager`).

## Run with Docker

Every merge to `main` and every version tag publishes the image to GHCR. The package is
private, so log in with a GitHub token that has `read:packages`, pull it and give it the
short name the commands below use:

```bash
docker login ghcr.io
docker pull ghcr.io/esade-swdev-2026/library-manager:v1.0
docker tag ghcr.io/esade-swdev-2026/library-manager:v1.0 library-manager
```

Or build it yourself from the repo with `docker build -t library-manager .`. Either way:

```bash
docker run --rm library-manager --help
docker run --rm -v library-manager-data:/app/data library-manager borrow "Dune"
docker run --rm -v library-manager-data:/app/data library-manager show
docker run --rm -it -v library-manager-data:/app/data library-manager menu
docker run --rm -v library-manager-data:/app/data library-manager locsv /app/data/my_books.csv
```

Every `docker run --rm` starts a fresh container, so anything that is not in a volume is
lost when the command ends. The named volume `library-manager-data`, mounted on
`/app/data`, keeps two things:

- the books: the first time it is used, Docker fills it with `data/example_books.csv`, and
  every loan or return is saved there;
- the csv you chose with `locsv`, stored in `/app/data/.library_manager`.

**Always include `-v library-manager-data:/app/data`** in commands that change something.
Without it, loans and your `locsv` choice are lost as soon as the container exits.

`docker volume rm library-manager-data` deletes both and starts again from the example
books. The volume is only filled from the image the first time, so if the example books
change in a new version, existing volumes keep the old copy until you remove them.

### Using your own csv in Docker

Either copy your csv into the volume, or mount the folder that contains it and select it
with `locsv` using the path as seen *inside* the container:

```bash
docker run --rm -v library-manager-data:/app/data -v "$PWD/mybooks:/books" library-manager locsv /books/mine.csv
```

With a bind mount like this, you must mount `/books` again in every later command;
otherwise the saved path does not exist in the container.

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
  library.py           borrowing, renewing and returning rules
  book.py              the Book dataclass
  storage.py           loads and saves the books CSV
  interface.py         formats the books as a table
  __main__.py          lets `python -m library_manager` work
data/                  example_books.csv, the books the app starts from
Dockerfile             builds the container image
scripts/check.sh       runs the four checks
tests/                 pytest tests, mirroring src/
pyproject.toml         dependencies and tool configuration — the single source of truth
```
## Features

- **Show available books** (`show`) — list all books in the library with their copies left.
- **Book description** (`description`) — see what a book is about.
- **Search by author** (`afilter`) — list every book by an author.
- **Filter by genre** (`gfilter`) — narrow the book list down to a genre.
- **Filter by language** (`filter`) — narrow the book list down to a language (Spanish, French, Catalan, English, ...).
- **Borrow** (`borrow`) — borrow a copy of a book for 30 days.
- **Renew** (`renew`) — extend the due date before it expires, so you don't have to return a book you haven't finished.
- **Return** (`return`) — give back a borrowed book; tells you if it was returned late.
- **Your own books** (`locsv`) — use your own csv instead of the example one.
- **Menu** (`menu`) — show, borrow, return, renew, filter and read descriptions from one interactive menu.


## Use of Artificial Intelligence

- **Understanding** — At the start of the project, we used AI to help us understand functions like `find_book` and `find_book_by_author` and what they were used for, before coding them ourselves.
- **Commands & Prompts** — When we got stuck and forgot the exact command for a specific action, we asked the AI for it so we could solve the problem efficiently.
- **Books CSV** — To create our sample dataset, we used AI to generate a list of real existing books with their corresponding author, in the correct table format (name, author, quantity, language, description).
- **Writing Tests** — AI helped us write some of the more repetitive tests, once we understood the pattern and had coded several of them ourselves.
- **Shell Tests** — AI also helped us write tests for our shell scripts, such as checking that a given string is returned unchanged.
- **Edge Cases** — AI helped us identify edge cases for our tests that we hadn't initially considered.
- **PR and Docker Issues** — We also used AI when our PR wasn't updating correctly and when we had issues with the Dockerfile. It suggested commands such as `git checkout main`, `git pull`, and `git fetch --prune` to fix the syncing problems between our branch and the PR.