"""Wizard component for console UI"""

from dataclasses import dataclass, field
from typing import Any

from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.keys import Key


@dataclass
class WizardStep:
    """Wizard step configuration"""

    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class Wizard(Component):
    """Wizard component for step-by-step interfaces"""

    def __init__(self) -> None:
        config = ComponentConfig(
            x=0,
            y=0,
            width=80,
            height=24,
            style={
                "title": Style(color="blue", bold=True),
                "content": Style(color="white"),
                "navigation": Style(color="cyan"),
            },
        )
        super().__init__(config=config)
        self.steps: list[WizardStep] = []
        self.current_step = 0

    def add_step(self, title: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Add step to wizard"""
        self.steps.append(WizardStep(title=title, content=content, metadata=metadata or {}))

    def next_step(self) -> bool:
        """Move to next step"""
        if not self.config.visible or self.current_step >= len(self.steps) - 1:
            return False
        self.current_step += 1
        return True

    def previous_step(self) -> bool:
        """Move to previous step"""
        if not self.config.visible or self.current_step <= 0:
            return False
        self.current_step -= 1
        return True

    def render(self) -> Text:
        """Render wizard"""
        if not self.steps or not self.config.visible:
            return Text()

        text = Text()
        step = self.steps[self.current_step]

        # Render title
        title = f"Step {self.current_step + 1}/{len(self.steps)}: {step.title}"
        text.append(
            f"{' ' * self.config.x}{title}\n",
            style=self.config.style.get("title", Style()),
        )

        # Render content
        content_lines = step.content.split("\n")
        for line in content_lines:
            text.append(
                f"{' ' * self.config.x}{line}\n",
                style=self.config.style.get("content", Style()),
            )

        # Render navigation
        nav_text = []
        if self.current_step > 0:
            nav_text.append("← Previous")
        if self.current_step < len(self.steps) - 1:
            nav_text.append("Next →")

        if nav_text:
            text.append(
                f"{' ' * self.config.x}{' | '.join(nav_text)}",
                style=self.config.style.get("navigation", Style()),
            )

        return text

    async def handle_input(self, key: Key) -> bool:
        """Handle input event"""
        if not self.config.visible:
            return False

        if key == Key.LEFT and self.current_step > 0:
            return self.previous_step()
        if key == Key.RIGHT and self.current_step < len(self.steps) - 1:
            return self.next_step()

        return False
