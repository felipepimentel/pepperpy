"""Toast component"""

from dataclasses import dataclass
from enum import Enum

from .base import Component


class ToastType(str, Enum):
    """Toast types"""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Toast(Component):
    """Toast notification component"""

    message: str
    type: ToastType = ToastType.INFO
    duration: float = 3.0
