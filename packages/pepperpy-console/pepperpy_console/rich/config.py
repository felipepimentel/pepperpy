"""Rich console configuration"""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class RichConfig:
    """Rich console specific configuration"""

    style: str = "default"
    highlight: bool = True
    markup: bool = True
    emoji: bool = True
    color_system: Literal[
        "auto", "standard", "256", "truecolor", "windows"
    ] | None = "truecolor"
    width: int | None = None
    height: int | None = None
    tab_size: int = 8
    soft_wrap: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
