"""Spinner component for console UI"""

import asyncio
import itertools
from typing import Any

from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.styles import styles


class Spinner(Component):
    """Animated spinner component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "spinner": Style(color="cyan", bold=True),
                "text": Style(color="white"),
            },
        )
        super().__init__(config=config)
        self._frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self._frame_iter = itertools.cycle(self._frames)
        self._running = False
        self._text = ""
        self._task: asyncio.Task[None] | None = None

    def start(self, text: str = "") -> None:
        """
        Start spinner animation

        Args:
            text: Text to display next to spinner

        """
        self._text = text
        self._running = True
        if not self._task:
            self._task = asyncio.create_task(self._animate())

    def stop(self) -> None:
        """Stop spinner animation"""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None

    async def _animate(self) -> None:
        """Animate spinner"""
        try:
            while self._running:
                await asyncio.sleep(0.1)
                next(self._frame_iter)
        except asyncio.CancelledError:
            pass

    def render(self) -> Text:
        """
        Render spinner

        Returns:
            Text: Rendered spinner

        """
        text = Text()
        frame = next(self._frame_iter) if self._running else "●"

        # Render spinner
        text.append(frame, style=styles.apply("primary"))

        # Render text
        if self._text:
            text.append(f" {self._text}", style=styles.apply("default"))

        return text

    def __enter__(self) -> "Spinner":
        """Enter context manager"""
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager"""
        self.stop()
