"""Spinner component implementation"""

import asyncio
from typing import List, Optional

from ..styles import Style
from .base import Component, ComponentConfig


class Spinner(Component):
    """Animated spinner component"""

    DEFAULT_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(
        self,
        config: ComponentConfig,
        text: str = "",
        frames: Optional[List[str]] = None,
        interval: float = 0.1,
    ):
        super().__init__(config)
        self.text = text
        self.frames = frames or self.DEFAULT_FRAMES
        self.interval = interval
        self._frame_index = 0
        self._running = False
        self._task = None

    async def start(self) -> None:
        """Start spinner animation"""
        self._running = True
        self._task = asyncio.create_task(self._animate())

    async def stop(self) -> None:
        """Stop spinner animation"""
        self._running = False
        if self._task:
            await self._task

    async def _animate(self) -> None:
        """Animate spinner"""
        while self._running:
            await self.render()
            self._frame_index = (self._frame_index + 1) % len(self.frames)
            await asyncio.sleep(self.interval)

    async def _setup(self) -> None:
        """Initialize spinner"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup spinner"""
        await self.stop()

    async def render(self) -> None:
        """Render spinner frame"""
        if not self.config.visible:
            return

        style = self.config.style or Style()

        # Move cursor and clear line
        print(f"\033[{self.config.y};{self.config.x}H\033[K", end="")

        # Render current frame and text
        frame = self.frames[self._frame_index]
        print(f"{style.apply()}{frame} {self.text}{style.reset()}", end="")
