from dataclasses import dataclass
from typing import Optional

from rich.progress import Progress as RichProgress
from rich.progress import TaskID
from rich.status import Status as RichStatus


@dataclass
class Progress:
    """Enhanced progress bar wrapper"""

    def __init__(self, console):
        self._progress = RichProgress(console=console)

    def add_task(self, description: str, total: Optional[float] = None) -> TaskID:
        """Add a new task to the progress bar

        Args:
            description: Task description
            total: Total steps for the task

        Returns:
            TaskID: Identifier for the created task
        """
        return self._progress.add_task(description, total=total)

    def update(self, task_id: TaskID, advance: Optional[float] = None) -> None:
        """Update task progress

        Args:
            task_id: Task identifier
            advance: Amount to advance the task
        """
        self._progress.update(task_id, advance=advance)


@dataclass
class Status:
    """Enhanced status indicator"""

    def __init__(self, console):
        self._status = RichStatus(console=console)

    def update(self, status: str) -> None:
        """Update status message

        Args:
            status: New status message to display
        """
        self._status.update(status)
