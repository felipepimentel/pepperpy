"""Progress bar component"""

from dataclasses import dataclass
from typing import Any, Callable

from rich.progress import BarColumn, TaskID, TextColumn, TimeRemainingColumn
from rich.progress import Progress as RichProgress

from .base import Component


@dataclass
class ProgressConfig:
    """Progress bar configuration"""

    total: float = 100.0
    description: str = ""
    unit: str = "%"
    style: str = "default"
    show_percentage: bool = True
    show_speed: bool = False
    show_time: bool = True
    auto_refresh: bool = True
    callback: Callable[[float], None] | None = None


class ProgressBar(Component):
    """Progress bar component"""

    def __init__(self, config: ProgressConfig | None = None):
        super().__init__()
        self.config = config or ProgressConfig()

        columns = [
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
        ]

        if self.config.show_percentage:
            columns.append(TextColumn("[progress.percentage]{task.percentage:>3.0f}%"))

        if self.config.show_speed:
            columns.append(TextColumn("Speed: {task.speed:.2f}{task.unit}/s"))

        if self.config.show_time:
            columns.append(TimeRemainingColumn())

        self._progress = RichProgress(*columns, auto_refresh=self.config.auto_refresh)
        self._task_id: TaskID | None = None
        self._current: float = 0.0

    async def initialize(self) -> None:
        """Initialize progress bar"""
        await super().initialize()
        self._task_id = self._progress.add_task(
            self.config.description, total=self.config.total, unit=self.config.unit
        )

    @property
    def current(self) -> float:
        """Get current progress value"""
        return self._current

    @current.setter
    def current(self, value: float) -> None:
        """Update progress value"""
        self._current = min(max(0.0, value), self.config.total)
        if self._task_id is not None:
            self._progress.update(self._task_id, completed=self._current)
            if self.config.callback:
                self.config.callback(self._current / self.config.total)

    async def render(self) -> Any:
        """Render progress bar"""
        await super().render()
        return self._progress
