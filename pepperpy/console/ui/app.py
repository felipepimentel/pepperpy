"""Console application management"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from pepperpy.core.logging import get_logger
from pepperpy.core.module import BaseModule, ModuleMetadata

from .components.base import Component
from .exceptions import UIError
from .keyboard import Key, KeyboardManager, KeyEvent
from .layout import Direction, Layout
from .screen import Screen
from .styles import Theme


@dataclass
class AppConfig:
    """Configuration for console application"""

    title: str
    theme: Optional[Theme] = None
    width: Optional[int] = None
    height: Optional[int] = None
    debug: bool = False
    auto_refresh: bool = True
    refresh_rate: float = 0.01
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConsoleApp(BaseModule):
    """High-level console application manager"""

    def __init__(self, config: AppConfig):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="console_app",
            version="1.0.0",
            description="Console UI application",
            dependencies=["rich>=13.0.0"],
            config=config.__dict__,
        )
        self._screen: Optional[Screen] = None
        self._layout: Optional[Layout] = None
        self._components: List[Component] = []
        self._running = False
        self._refresh_task: Optional[asyncio.Task] = None
        self._logger = get_logger(__name__)

    async def _setup(self) -> None:
        """Initialize application"""
        try:
            # Create main screen
            self._screen = Screen(
                title=self.config["title"],
                theme=self.config.get("theme"),
                width=self.config.get("width"),
                height=self.config.get("height"),
            )

            # Create main layout
            self._layout = Layout(config=self._screen.config, direction=Direction.VERTICAL)

            await self._screen.initialize()
            await self._layout.initialize()

            # Initialize components
            for component in self._components:
                await component.initialize()

        except Exception as e:
            raise UIError("Failed to initialize console application", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup application resources"""
        try:
            # Stop refresh task
            if self._refresh_task:
                self._refresh_task.cancel()
                try:
                    await self._refresh_task
                except asyncio.CancelledError:
                    pass

            # Cleanup components
            for component in self._components:
                await component.cleanup()

            # Cleanup layout and screen
            if self._layout:
                await self._layout.cleanup()
            if self._screen:
                await self._screen.cleanup()

        except Exception as e:
            await self._logger.error(f"Error during cleanup: {str(e)}")

    async def run(self) -> None:
        """Run application main loop"""
        if not self._screen or not self._layout:
            raise UIError("Application not initialized")

        try:
            self._running = True

            # Start auto-refresh if enabled
            if self.config.get("auto_refresh", True):
                self._refresh_task = asyncio.create_task(self._auto_refresh())

            with KeyboardManager() as kb:
                while self._running:
                    # Handle input
                    key = kb.get_key()
                    if key.key == Key.CTRL_C:
                        break

                    await self._handle_input(key)

                    # Manual refresh if auto-refresh disabled
                    if not self.config.get("auto_refresh", True):
                        await self._render()

                    # Small delay to prevent high CPU usage
                    await asyncio.sleep(0.01)

        except Exception as e:
            await self._logger.error(f"Error in main loop: {str(e)}")
            raise UIError("Application error", cause=e)
        finally:
            self._running = False
            await self.cleanup()

    async def add_component(
        self, component: Component, layout_constraints: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add component to application"""
        self._components.append(component)
        if self._layout:
            self._layout.add(component, layout_constraints)
            if self._running:
                await component.initialize()

    async def remove_component(self, component: Component) -> None:
        """Remove component from application"""
        if component in self._components:
            self._components.remove(component)
            if self._layout:
                self._layout.remove(component)
            await component.cleanup()

    async def _handle_input(self, key: KeyEvent) -> None:
        """Handle keyboard input"""
        try:
            # Log debug info
            if self.config.get("debug"):
                await self._logger.debug(f"Key pressed: {key.key}")

            # Delegate to active component if any
            for component in self._components:
                if hasattr(component, "handle_input"):
                    if await component.handle_input(key):
                        break

        except Exception as e:
            await self._logger.error(f"Error handling input: {str(e)}")

    async def _render(self) -> None:
        """Render application"""
        try:
            await self._screen.clear()
            await self._layout.render()
            await self._screen.refresh()
        except Exception as e:
            await self._logger.error(f"Error rendering: {str(e)}")

    async def _auto_refresh(self) -> None:
        """Auto refresh loop"""
        try:
            while self._running:
                await self._render()
                await asyncio.sleep(self.config.get("refresh_rate", 0.01))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self._logger.error(f"Error in refresh loop: {str(e)}")
