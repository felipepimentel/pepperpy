"""AI module for PepperPy"""

from .chat import Conversation

# Convenience functions
from .client import AIClient, AIConfig, AIResponse, ask, complete, stream
from .exceptions import AIError

__all__ = [
    "AIClient",
    "AIConfig",
    "AIResponse",
    "AIError",
    "Conversation",
    "ask",
    "complete",
    "stream",
]
