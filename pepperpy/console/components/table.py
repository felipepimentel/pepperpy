"""Table component for console output"""

from typing import List, Optional

from rich.table import Table as RichTable


class Table:
    """Enhanced table component"""

    def __init__(self, console):
        self._console = console
        self._table = RichTable()

    def add_column(self, header: str, style: Optional[str] = None) -> None:
        """Add column with optional styling

        Args:
            header: Column header text
            style: Optional style string
        """
        self._table.add_column(header, style=style)

    def add_row(self, *values: str, style: Optional[str] = None) -> None:
        """Add row with optional styling

        Args:
            *values: Row values
            style: Optional style string
        """
        self._table.add_row(*values, style=style)

    def from_records(self, records: List[dict], columns: Optional[List[str]] = None) -> None:
        """Create table from list of dictionaries

        Args:
            records: List of dictionaries containing data
            columns: Optional list of column names to include
        """
        if not records:
            return

        # Get columns from first record if not specified
        cols = columns or list(records[0].keys())

        # Add columns
        for col in cols:
            self.add_column(str(col))

        # Add rows
        for record in records:
            self.add_row(*[str(record[col]) for col in cols])

    def render(self) -> None:
        """Render table to console"""
        self._console.print(self._table)
