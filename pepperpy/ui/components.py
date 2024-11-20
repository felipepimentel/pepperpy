"""UI components implementation"""

from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Optional

TaskCallback = Callable[[], Coroutine[Any, Any, None]]


@dataclass
class Component:
    """Base UI component"""

    title: str
    style: str = "default"

    async def render(self) -> str:
        """Render component"""
        return f"[{self.style}]{self.title}[/{self.style}]"


@dataclass
class Panel(Component):
    """Panel component"""

    content: Optional[str] = None

    async def render(self) -> str:
        """Render panel"""
        result = [f"╔{'═' * (len(self.title) + 2)}╗"]
        result.append(f"║ {self.title} ║")
        result.append(f"╚{'═' * (len(self.title) + 2)}╝")
        if self.content:
            result.append(self.content)
        return "\n".join(result)


@dataclass
class Progress(Component):
    """Progress component"""

    description: str = ""
    current: int = 0
    total: int = 100

    async def render(self) -> str:
        """Render progress bar"""
        width = 50
        filled = int(width * self.current / self.total)
        bar = "█" * filled + "░" * (width - filled)
        percent = self.current / self.total * 100
        return f"{self.description} [{bar}] {percent:.1f}%"

    def set_progress(self, value: int, description: Optional[str] = None) -> None:
        """Update progress value"""
        self.current = min(value, self.total)
        if description is not None:
            self.description = description


@dataclass
class Button:
    """Button component"""

    label: str
    callback: TaskCallback
    style: str = "default"

    async def render(self) -> str:
        """Render button"""
        return f"[{self.style}]{self.label}[/{self.style}]"


@dataclass
class Form(Component):
    """Form component"""

    buttons: list[Button] = field(default_factory=list)

    async def initialize(self) -> None:
        """Initialize form"""
        pass

    def add_button(self, label: str, callback: TaskCallback, style: str = "default") -> None:
        """Add button to form"""
        self.buttons.append(Button(label=label, callback=callback, style=style))

    async def render(self) -> str:
        """Render form"""
        result = [f"=== {self.title} ==="]
        for button in self.buttons:
            result.append(await button.render())
        return "\n".join(result)


@dataclass
class Dialog(Component):
    """Dialog component"""

    buttons: list[Button] = field(default_factory=list)
    message: str = ""

    def add_button(self, label: str, callback: TaskCallback, style: str = "default") -> None:
        """Add button to dialog"""
        self.buttons.append(Button(label=label, callback=callback, style=style))

    async def render(self) -> str:
        """Render dialog"""
        width = max(len(self.title), len(self.message)) + 4
        result = [
            f"╔{'═' * width}╗",
            f"║ {self.title.center(width-2)} ║",
            f"║ {' ' * (width-2)} ║",
            f"║ {self.message.center(width-2)} ║",
            f"║ {' ' * (width-2)} ║",
        ]
        for button in self.buttons:
            rendered = await button.render()
            result.append(f"║ {rendered.center(width-2)} ║")
        result.append(f"╚{'═' * width}╝")
        return "\n".join(result) 