"""Dialog component for interactive prompts"""

from dataclasses import dataclass
from typing import Any, Callable

from rich.panel import Panel as RichPanel

from .base import Component


@dataclass
class DialogButton:
    """Dialog button configuration"""
    label: str
    callback: Callable[[], None]
    style: str = "default"

class Dialog(Component):
    """Dialog component"""
    
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.content: Any = ""
        self._buttons: list[DialogButton] = []
        
    def add_button(self, label: str, callback: Callable[[], None], 
                  style: str = "default") -> None:
        """Add button to dialog"""
        self._buttons.append(DialogButton(label, callback, style))
        
    async def render(self) -> Any:
        """Render dialog"""
        await super().render()
        
        # Render buttons
        buttons_text = " ".join(
            f"[{btn.style}]{btn.label}[/]" 
            for btn in self._buttons
        )
        
        # Combine content and buttons
        full_content = f"{self.content}\n\n{buttons_text}"
        
        return RichPanel(
            full_content,
            title=self.title,
            border_style="bold",
            padding=(1, 2)
        ) 