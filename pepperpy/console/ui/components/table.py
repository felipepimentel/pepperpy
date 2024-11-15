"""Table component"""

from dataclasses import dataclass
from typing import Any, Literal

from rich.style import Style
from rich.table import Table as RichTable
from rich.text import Text

from .base import Component, ComponentConfig

JustifyMethod = Literal["left", "center", "right", "full"]


@dataclass
class Column:
    """Table column configuration"""

    header: str
    style: str | None = None
    align: JustifyMethod = "left"
    show_header: bool = True


class Table(Component):
    """Table component for displaying tabular data"""

    def __init__(
        self, columns: list[Column] | None = None, data: list[list[str]] | None = None,
    ):
        config = ComponentConfig(
            style={
                "header": Style(bold=True),
                "cell": Style(),
                "border": Style(dim=True),
            },
        )
        super().__init__(config)
        self._columns: list[Column] = columns or []
        self._data: list[list[str]] = data or []

    async def initialize(self) -> None:
        """Initialize table"""

    async def cleanup(self) -> None:
        """Cleanup table"""

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        return False

    def add_column(
        self,
        header: str,
        style: str | None = None,
        align: JustifyMethod = "left",
        show_header: bool = True,
    ) -> None:
        """Add a column to the table"""
        self._columns.append(
            Column(header=header, style=style, align=align, show_header=show_header),
        )

    def add_row(self, *values: str) -> None:
        """Add a row to the table"""
        self._data.append(list(values))

    def render(self) -> Text:
        """Render table"""
        table = RichTable(show_header=any(col.show_header for col in self._columns))

        # Add columns
        for col in self._columns:
            table.add_column(
                col.header if col.show_header else "",
                style=col.style,
                justify=col.align,
            )

        # Add rows
        for row in self._data:
            table.add_row(*row)

        return Text.from_markup(str(table))
