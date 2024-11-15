"""CLI configuration"""

from dataclasses import dataclass


@dataclass
class CLIConfig:
    """Configuration for CLI applications"""

    name: str = "app"
    description: str = ""
    version: str = "1.0.0"
    author: str | None = None
    help_text: str | None = None
