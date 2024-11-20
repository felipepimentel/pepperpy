"""Console module"""

import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ConsoleMessage:
    """Console message"""

    text: str
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Console:
    """Console interface"""

    async def info(self, message: str, title: Optional[str] = None, content: Optional[str] = None) -> None:
        """Log info message"""
        print(f"\n{'='*50}")
        if title:
            print(f"{title}")
            print(f"{'='*50}")
        print(message)
        if content:
            print(f"\n{content}")
        print(f"{'='*50}\n")

    async def success(self, message: str, title: Optional[str] = None, content: Optional[str] = None) -> None:
        """Log success message"""
        print(f"\n{'='*50}")
        if title:
            print(f"✅ {title}")
            print(f"{'='*50}")
        print(message)
        if content:
            print(f"\n{content}")
        print(f"{'='*50}\n")

    async def error(self, message: str, error: Optional[str] = None) -> None:
        """Log error message"""
        print(f"\n{'='*50}")
        print(f"❌ {message}")
        if error:
            print(f"Error: {error}")
        print(f"{'='*50}\n")

    async def warning(self, message: str, title: Optional[str] = None) -> None:
        """Log warning message"""
        print(f"\n{'='*50}")
        if title:
            print(f"⚠️ {title}")
            print(f"{'='*50}")
        print(message)
        print(f"{'='*50}\n")

    async def print(self, message: str) -> None:
        """Print message"""
        print(message)

    async def clear(self) -> None:
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')
