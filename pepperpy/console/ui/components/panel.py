"""Panel component for content framing"""

from dataclasses import dataclass
from typing import Any

from rich.panel import Panel as RichPanel

from .base import Component


@dataclass
class PanelConfig:
    """Panel configuration"""
    title: str = ""
    subtitle: str = ""
    style: str = "default"
    border_style: str = "default"
    padding: tuple[int, int] = (1, 1)

class Panel(Component):
    """Panel component for framing content"""
    
    def __init__(self, content: Any, config: PanelConfig | None = None):
        super().__init__()
        self.content = content
        self.config = config or PanelConfig()
        
    async def initialize(self) -> None:
        """Initialize panel"""
        await super().initialize()
        if isinstance(self.content, Component):
            await self.content.initialize()
            
    async def render(self) -> Any:
        """Render panel"""
        await super().render()
        content = (
            await self.content.render() 
            if isinstance(self.content, Component) 
            else self.content
        )
        return RichPanel(
            content,
            title=self.config.title,
            subtitle=self.config.subtitle,
            style=self.config.style,
            border_style=self.config.border_style,
            padding=self.config.padding
        )
        
    async def cleanup(self) -> None:
        """Cleanup panel resources"""
        if isinstance(self.content, Component):
            await self.content.cleanup()
        await super().cleanup() 