"""Console UI application"""

import asyncio
from typing import Dict, Optional, Set

from pepperpy.core.logging import get_logger

from .components.base import Component
from .exceptions import UIError
from .keyboard import CTRL_C, Key, KeyboardManager
from .layout import Layout
from .screen import Screen, ScreenConfig


class ConsoleApp:
    """Console UI application"""

    def __init__(self):
        self._logger = get_logger(__name__)
        self._screen: Optional[Screen] = None
        self._layout: Optional[Layout] = None
        self._keyboard = KeyboardManager()
        self._running = False
        self._components: Dict[str, Component] = {}
        self._tasks: Set[asyncio.Task] = set()

    async def initialize(self) -> None:
        """Initialize application"""
        try:
            # Initialize screen
            config = ScreenConfig(
                width=80,
                height=24,
                title="PepperPy Console",
            )
            self._screen = Screen(config)
            await self._screen.initialize()

            # Initialize layout
            self._layout = Layout()
            await self._layout.initialize()

            # Initialize keyboard
            await self._keyboard.initialize()

            # Initialize components
            for component in self._components.values():
                await component.initialize()

        except Exception as e:
            raise UIError(f"Failed to initialize application: {str(e)}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup application"""
        try:
            # Cancel all tasks
            for task in self._tasks:
                task.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            self._tasks.clear()

            # Cleanup components
            for component in self._components.values():
                await component.cleanup()

            # Cleanup layout
            if self._layout:
                await self._layout.cleanup()

            # Cleanup screen
            if self._screen:
                await self._screen.cleanup()

            # Cleanup keyboard
            await self._keyboard.cleanup()

        except Exception as e:
            raise UIError(f"Failed to cleanup application: {str(e)}", cause=e)

    async def run(self) -> None:
        """Run application"""
        try:
            await self.initialize()
            self._running = True

            while self._running:
                # Handle input
                key = await self._keyboard.get_key()
                if key == CTRL_C:
                    self._running = False
                    continue

                # Handle component input
                for component in self._components.values():
                    if await component.handle_input(key):
                        break

                # Render screen
                await self.render()

                # Sleep to prevent high CPU usage
                await asyncio.sleep(0.01)

        except asyncio.CancelledError:
            self._running = False
        except Exception as e:
            raise UIError(f"Application error: {str(e)}", cause=e)
        finally:
            await self.cleanup()

    def add_component(self, name: str, component: Component) -> None:
        """Add component to application"""
        if name in self._components:
            raise UIError(f"Component already exists: {name}")

        self._components[name] = component
        if self._layout:
            self._layout.add(component)
            if self._running:
                task = asyncio.create_task(component.initialize())
                self._tasks.add(task)

    def remove_component(self, name: str) -> None:
        """Remove component from application"""
        if name not in self._components:
            return

        component = self._components.pop(name)
        if self._layout:
            self._layout.remove(component)
            if self._running:
                task = asyncio.create_task(component.cleanup())
                self._tasks.add(task)

    async def handle_input(self, key: Key) -> bool:
        """Handle input event"""
        for component in self._components.values():
            if await component.handle_input(key):
                return True
        return False

    async def render(self) -> None:
        """Render application"""
        if not self._screen or not self._layout:
            return

        self._screen.clear()
        text = self._layout.render()
        self._screen.print(text)
        self._screen.refresh()


# Global application instance
app = ConsoleApp()
