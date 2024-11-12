"""Progress bar component implementation"""

from typing import Optional

from ..styles import Style
from .base import Component, ComponentConfig


class ProgressBar(Component):
    """Progress bar component"""

    def __init__(
        self,
        config: ComponentConfig,
        total: int = 100,
        label: Optional[str] = None,
        show_percentage: bool = True,
        fill_char: str = "█",
        empty_char: str = "░",
    ):
        super().__init__(config)
        self.total = total
        self.label = label
        self.show_percentage = show_percentage
        self.fill_char = fill_char
        self.empty_char = empty_char
        self._value = 0

    @property
    def value(self) -> int:
        """Get current progress value"""
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        """Set progress value"""
        self._value = max(0, min(new_value, self.total))

    @property
    def percentage(self) -> float:
        """Get progress percentage"""
        return (self._value / self.total) * 100 if self.total > 0 else 0

    async def _setup(self) -> None:
        """Initialize progress bar"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup progress bar"""
        pass

    async def render(self) -> None:
        """Render progress bar"""
        if not self.config.visible:
            return

        # Move cursor
        print(f"\033[{self.config.y};{self.config.x}H", end="")

        # Apply styles
        style = self.config.style or Style()

        # Render label if present
        if self.label:
            print(f"{self.label}: ", end="")

        # Calculate bar width
        width = self.config.width or 50
        filled_width = int((self._value / self.total) * width)

        # Render bar
        bar = (
            f"{style.apply()}"
            f"{self.fill_char * filled_width}"
            f"{self.empty_char * (width - filled_width)}"
            f"{style.reset()}"
        )
        print(bar, end="")

        # Show percentage
        if self.show_percentage:
            print(f" {self.percentage:.1f}%")
        else:
            print()
