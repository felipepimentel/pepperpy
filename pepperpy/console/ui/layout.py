"""Layout management for UI components"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pepperpy.core.logging import get_logger
from pepperpy.core.module import BaseModule, ModuleMetadata

from .components.base import Component, ComponentConfig
from .exceptions import UIError


class Direction(Enum):
    """Layout direction"""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class LayoutConstraints:
    """Layout constraints for components"""

    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    flex: int = 1
    margin: Tuple[int, int, int, int] = (0, 0, 0, 0)  # top, right, bottom, left
    align: str = "start"  # start, center, end
    expand: bool = False


@dataclass
class LayoutConfig:
    """Configuration for layout"""

    direction: Direction = Direction.VERTICAL
    spacing: int = 1
    padding: Tuple[int, int, int, int] = (0, 0, 0, 0)
    debug: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class Layout(BaseModule):
    """Layout manager for organizing components"""

    def __init__(self, config: ComponentConfig, layout_config: Optional[LayoutConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="layout",
            version="1.0.0",
            description="UI layout management",
            dependencies=[],
            config=config.__dict__,
        )
        self._layout_config = layout_config or LayoutConfig()
        self._components: List[Tuple[Component, LayoutConstraints]] = []
        self._logger = get_logger(__name__)

    async def _setup(self) -> None:
        """Initialize layout"""
        try:
            # Initialize components
            for component, _ in self._components:
                await component.initialize()
        except Exception as e:
            raise UIError("Failed to initialize layout", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup layout resources"""
        try:
            # Cleanup components
            for component, _ in self._components:
                await component.cleanup()
        except Exception as e:
            await self._logger.error(f"Error during cleanup: {str(e)}")

    def add(self, component: Component, constraints: Optional[LayoutConstraints] = None) -> None:
        """Add component with constraints"""
        self._components.append((component, constraints or LayoutConstraints()))

    def remove(self, component: Component) -> None:
        """Remove component from layout"""
        self._components = [(c, const) for c, const in self._components if c != component]

    async def render(self) -> None:
        """Render layout and components"""
        try:
            # Calculate layout
            self._calculate_layout()

            # Render components
            for component, _ in self._components:
                await component.render()

            # Debug rendering if enabled
            if self._layout_config.debug:
                self._render_debug()

        except Exception as e:
            await self._logger.error(f"Error rendering layout: {str(e)}")

    def _calculate_layout(self) -> None:
        """Calculate component positions and sizes"""
        try:
            available_width = self.config.get("width", 80)
            available_height = self.config.get("height", 24)
            current_x = self.config.get("x", 0)
            current_y = self.config.get("y", 0)

            # Apply padding
            pad_top, pad_right, pad_bottom, pad_left = self._layout_config.padding
            available_width -= pad_left + pad_right
            available_height -= pad_top + pad_bottom
            current_x += pad_left
            current_y += pad_top

            if self._layout_config.direction == Direction.HORIZONTAL:
                self._calculate_horizontal(current_x, current_y, available_width, available_height)
            else:
                self._calculate_vertical(current_x, current_y, available_width, available_height)

        except Exception as e:
            raise UIError(f"Layout calculation failed: {str(e)}", cause=e)

    def _calculate_horizontal(self, start_x: int, start_y: int, width: int, height: int) -> None:
        """Calculate horizontal layout"""
        # Calculate total flex and fixed widths
        total_flex = sum(c.flex for _, c in self._components if not c.max_width)
        fixed_width = sum(c.max_width or 0 for _, c in self._components if c.max_width)
        spacing_width = self._layout_config.spacing * (len(self._components) - 1)

        # Calculate flex unit
        available_width = max(0, width - fixed_width - spacing_width)
        flex_unit = available_width / total_flex if total_flex > 0 else 0

        current_x = start_x
        for component, _ in self._components:
            # Calculate component width
            if component.constraints.max_width:
                comp_width = min(
                    component.constraints.max_width,
                    max(component.constraints.min_width or 0, width),
                )
            else:
                comp_width = max(
                    component.constraints.min_width or 0,
                    int(component.constraints.flex * flex_unit),
                )

            # Calculate vertical position
            if component.constraints.align == "center":
                comp_y = start_y + (height - comp_width) // 2
            elif component.constraints.align == "end":
                comp_y = start_y + height - comp_width
            else:
                comp_y = start_y

            # Apply margins
            top, right, bottom, left = component.constraints.margin
            comp_x = current_x + left
            comp_y += top
            comp_width = max(0, comp_width - left - right)
            comp_height = max(0, height - top - bottom)

            # Update component config
            component.config.x = comp_x
            component.config.y = comp_y
            component.config.width = comp_width
            component.config.height = comp_height if component.constraints.expand else None

            current_x += comp_width + self._layout_config.spacing

    def _calculate_vertical(self, start_x: int, start_y: int, width: int, height: int) -> None:
        """Calculate vertical layout"""
        # Similar to horizontal but for vertical layout
        total_flex = sum(c.flex for _, c in self._components if not c.max_height)
        fixed_height = sum(c.max_height or 0 for _, c in self._components if c.max_height)
        spacing_height = self._layout_config.spacing * (len(self._components) - 1)

        available_height = max(0, height - fixed_height - spacing_height)
        flex_unit = available_height / total_flex if total_flex > 0 else 0

        current_y = start_y
        for component, _ in self._components:
            if component.constraints.max_height:
                comp_height = min(
                    component.constraints.max_height,
                    max(component.constraints.min_height or 0, height),
                )
            else:
                comp_height = max(
                    component.constraints.min_height or 0,
                    int(component.constraints.flex * flex_unit),
                )

            if component.constraints.align == "center":
                comp_x = start_x + (width - comp_height) // 2
            elif component.constraints.align == "end":
                comp_x = start_x + width - comp_height
            else:
                comp_x = start_x

            top, right, bottom, left = component.constraints.margin
            comp_x += left
            comp_y = current_y + top
            comp_width = max(0, width - left - right)
            comp_height = max(0, comp_height - top - bottom)

            component.config.x = comp_x
            component.config.y = comp_y
            component.config.width = comp_width if component.constraints.expand else None
            component.config.height = comp_height

            current_y += comp_height + self._layout_config.spacing

    def _render_debug(self) -> None:
        """Render debug information"""
        if not self._layout_config.debug:
            return

        for component, _ in self._components:
            # Draw component bounds
            x, y = component.config.x, component.config.y
            w = component.config.width or 0
            h = component.config.height or 0

            print(f"\033[{y};{x}H+{'-' * (w-2)}+")
            for i in range(h - 2):
                print(f"\033[{y+i+1};{x}H|{' ' * (w-2)}|")
            print(f"\033[{y+h-1};{x}H+{'-' * (w-2)}+")

            # Print debug info
            info = f"{component.__class__.__name__} ({w}x{h})"
            print(f"\033[{y};{x+2}H{info}")
