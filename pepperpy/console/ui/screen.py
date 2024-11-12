"""Screen management for console UI"""

from dataclasses import dataclass, field
from typing import List, Optional

from pepperpy.core.module import BaseModule, ModuleMetadata

from .components import Component
from .exceptions import UIError
from .styles import Theme


@dataclass
class ScreenConfig:
    """Configuration for screen"""

    title: str
    theme: Theme
    width: int = 80
    height: int = 24
    components: List[Component] = field(default_factory=list)


class Screen(BaseModule):
    """Screen manager for console UI"""

    def __init__(self, config: Optional[ScreenConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="screen",
            version="1.0.0",
            description="Console screen management",
            dependencies=[],
            config=config.__dict__ if config else {},
        )
        self._components = []
        self._active = False

    async def _setup(self) -> None:
        """Initialize screen"""
        try:
            # Setup screen components
            for component in self.config.get("components", []):
                await component.initialize()
            self._active = True
        except Exception as e:
            raise UIError("Failed to initialize screen", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup screen resources"""
        for component in self._components:
            await component.cleanup()
        self._active = False

    async def render(self) -> None:
        """Render screen and components"""
        if not self._active:
            raise UIError("Screen not initialized")

        # Clear screen
        print("\033[2J\033[H")

        # Render components
        for component in self._components:
            await component.render()
