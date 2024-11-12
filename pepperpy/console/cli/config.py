"""CLI configuration"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CLIConfig:
    """Configuration for CLI applications"""

    name: str = "app"
    description: str = ""
    version: str = "1.0.0"
    author: Optional[str] = None
    help_text: Optional[str] = None
