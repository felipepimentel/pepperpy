"""UI styles"""

from enum import Enum
from typing import Optional

from .themes import Theme


class Style(str, Enum):
    """Style definitions"""

    DEFAULT = "default"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    HIGHLIGHT = "highlight"

    def apply(self, theme: Optional[Theme] = None) -> str:
        """Apply style using theme"""
        if not theme:
            return str(self.value)
        return theme.styles.get(self.value, self.value)
