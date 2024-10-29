# pypepper/console.py


def print_message(message: str):
    """Print a simple message to the console with rich styling."""
    from rich.console import Console  # Imported only when needed

    console = Console()
    console.print(message)


def print_table(data: list):
    """Print a table to the console based on provided data."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Data Table")

    # Assuming data is a list of dictionaries
    for column in data[0].keys():
        table.add_column(column)

    for row in data:
        table.add_row(*[str(value) for value in row.values()])

    console.print(table)
