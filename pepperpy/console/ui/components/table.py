"""Table component implementation"""

from dataclasses import dataclass
from typing import List, Optional

from ..styles import Style
from .base import Component, ComponentConfig


@dataclass
class Column:
    """Table column definition"""

    header: str
    width: Optional[int] = None
    align: str = "left"  # left, right, center


class Table(Component):
    """Table component for displaying data in columns"""

    def __init__(
        self,
        config: ComponentConfig,
        columns: List[Column],
        data: List[List[str]],
        show_header: bool = True,
        show_border: bool = True,
    ):
        super().__init__(config)
        self.columns = columns
        self.data = data
        self.show_header = show_header
        self.show_border = show_border
        self._calculate_widths()

    def _calculate_widths(self) -> None:
        """Calculate column widths"""
        for i, col in enumerate(self.columns):
            if col.width is None:
                # Get max width from data including header
                values = [str(row[i]) for row in self.data]
                if self.show_header:
                    values.append(col.header)
                col.width = max(len(v) for v in values)

    async def _setup(self) -> None:
        """Initialize table"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup table"""
        pass

    async def render(self) -> None:
        """Render table"""
        if not self.config.visible:
            return

        style = self.config.style or Style()
        y = self.config.y

        # Render header
        if self.show_header:
            if self.show_border:
                print(f"\033[{y};{self.config.x}H{style.apply()}┌", end="")
                for col in self.columns:
                    print("─" * (col.width + 2), end="┬")
                print("┐")
                y += 1

            print(f"\033[{y};{self.config.x}H", end="")
            for col in self.columns:
                if self.show_border:
                    print("│ ", end="")
                print(f"{col.header:<{col.width}}", end=" ")
            if self.show_border:
                print("│")
            else:
                print()
            y += 1

            if self.show_border:
                print(f"\033[{y};{self.config.x}H├", end="")
                for col in self.columns:
                    print("─" * (col.width + 2), end="┼")
                print("┤")
                y += 1

        # Render data
        for row in self.data:
            print(f"\033[{y};{self.config.x}H", end="")
            for i, value in enumerate(row):
                col = self.columns[i]
                if self.show_border:
                    print("│ ", end="")

                if col.align == "right":
                    print(f"{str(value):>{col.width}}", end=" ")
                elif col.align == "center":
                    print(f"{str(value):^{col.width}}", end=" ")
                else:
                    print(f"{str(value):<{col.width}}", end=" ")

            if self.show_border:
                print("│")
            else:
                print()
            y += 1

        # Bottom border
        if self.show_border:
            print(f"\033[{y};{self.config.x}H└", end="")
            for col in self.columns:
                print("─" * (col.width + 2), end="┴")
            print("┘")

        print(f"{style.reset()}")
