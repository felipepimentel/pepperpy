"""Key definitions for console UI"""

from enum import Enum, auto


class Key(Enum):
    """Key codes for console UI"""

    ENTER = auto()
    ESCAPE = auto()
    BACKSPACE = auto()
    TAB = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()

    @property
    def is_printable(self) -> bool:
        """Check if key is printable"""
        return hasattr(self, "char") and isinstance(self.char, str)

    @property
    def char(self) -> str:
        """Get character representation of key"""
        return getattr(self, "_char", "")
