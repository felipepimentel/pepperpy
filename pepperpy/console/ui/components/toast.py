"""Toast notification component"""

import asyncio
from enum import Enum
from typing import Optional

from ..styles import Style, Theme
from .base import Component, ComponentConfig


class ToastType(Enum):
    """Toast notification types"""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Toast(Component):
    """Temporary notification component"""

    def __init__(
        self,
        config: ComponentConfig,
        message: str,
        type: ToastType = ToastType.INFO,
        duration: float = 3.0,
        theme: Optional[Theme] = None,
    ):
        super().__init__(config)
        self.message = message
        self.type = type
        self.duration = duration
        self.theme = theme
        self._visible = False
        self._task = None

    async def show(self) -> None:
        """Show toast notification"""
        self._visible = True
        await self.render()
        self._task = asyncio.create_task(self._auto_hide())

    async def hide(self) -> None:
        """Hide toast notification"""
        self._visible = False
        # Clear notification area
        print(f"\033[{self.config.y};{self.config.x}H\033[K", end="")

    async def _auto_hide(self) -> None:
        """Automatically hide after duration"""
        await asyncio.sleep(self.duration)
        await self.hide()

    async def _setup(self) -> None:
        """Initialize toast"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup toast"""
        if self._task:
            self._task.cancel()
            await self.hide()

    async def render(self) -> None:
        """Render toast notification"""
        if not self._visible:
            return

        theme = self.theme or Theme(
            info=Style(fg_color=(100, 149, 237)),  # Cornflower Blue
            success=Style(fg_color=(50, 205, 50)),  # Lime Green
            warning=Style(fg_color=(255, 165, 0)),  # Orange
            error=Style(fg_color=(220, 20, 60)),  # Crimson
        )

        # Get style based on type
        style = getattr(theme, self.type.value)

        # Move cursor and clear line
        print(f"\033[{self.config.y};{self.config.x}H\033[K", end="")

        # Render notification
        icon = {
            ToastType.INFO: "ℹ",
            ToastType.SUCCESS: "✓",
            ToastType.WARNING: "⚠",
            ToastType.ERROR: "✗",
        }[self.type]

        print(f"{style.apply()}{icon} {self.message}{style.reset()}")
