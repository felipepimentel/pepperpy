"""Table component"""

from dataclasses import dataclass
from typing import Any, Literal

from rich.table import Table as RichTable

from .base import Component

# Define tipos válidos de alinhamento
JustifyMethod = Literal["left", "center", "right", "full"]


@dataclass
class Column:
    """Table column configuration"""

    header: str
    style: str | None = None
    align: JustifyMethod = "left"
    width: int | None = None


class Table(Component):
    """Table component"""

    def __init__(self):
        super().__init__()
        self._table = RichTable()
        self._columns: list[Column] = []
        self._rows: list[tuple[str, ...]] = []

    def add_column(
        self,
        header: str,
        *,
        style: str | None = None,
        align: JustifyMethod = "left",
        width: int | None = None,
    ) -> None:
        """Add column to table"""
        self._columns.append(Column(header, style, align, width))
        self._table.add_column(header, style=style, justify=align, width=width)

    def add_row(self, *values: str) -> None:
        """Add row to table"""
        self._rows.append(values)
        self._table.add_row(*values)

    async def render(self) -> Any:
        """Render table"""
        await super().render()
        return self._table
