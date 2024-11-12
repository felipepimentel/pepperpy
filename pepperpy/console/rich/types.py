"""Rich type definitions"""

from dataclasses import dataclass
from typing import Dict, Optional

from rich.style import Style


@dataclass
class RichTheme:
    """Rich theme configuration"""

    styles: Dict[str, Style]
    inherit: bool = True


@dataclass
class RichLayout:
    """Rich layout configuration"""

    name: str
    title: Optional[str] = None
    minimum_size: int = 1
    ratio: int = 1
    visible: bool = True
