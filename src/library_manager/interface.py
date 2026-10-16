from pathlib import Path

import pandas as pd
import typer


def print_terminal(csv_path: Path) -> None:
    book_df = pd.read_csv(csv_path).drop(columns="description").fillna("")
    # Left-align every column so long text reads naturally
    formatters = {
        column: f"{{:<{book_df[column].astype(str).str.len().max()}}}".format
        for column in book_df.columns
    }
    table = book_df.to_string(index=False, justify="left", formatters=formatters)
    header, *rows = table.splitlines()
    typer.echo(typer.style(header, fg=typer.colors.CYAN, bold=True))
    for row in rows:
        typer.echo(row)


"""
We used AI to format the table of the CSV
"""
