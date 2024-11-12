"""Rich configuration"""

from dataclasses import dataclass, field
from typing import Dict, List

from rich.progress import BarColumn, TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn


@dataclass
class RichConfig:
    """Configuration for rich applications"""

    # Theme configuration
    theme: Dict[str, str] = field(
        default_factory=lambda: {
            "info": "cyan",
            "warning": "yellow",
            "error": "red bold",
            "success": "green",
            "progress.description": "cyan",
            "progress.percentage": "green",
            "progress.remaining": "cyan",
            "table.header": "bold cyan",
            "panel.border": "cyan",
        }
    )

    # Style configuration
    header_style: str = "bold cyan"
    border_style: str = "cyan"
    panel_style: str = "cyan"
    code_theme: str = "monokai"

    # Progress configuration
    progress_columns: List = field(
        default_factory=lambda: [
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
        ]
    )

    # Display configuration
    refresh_rate: int = 15
    force_terminal: bool = False
    force_interactive: bool = False
    use_alternate_screen: bool = False
