from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..module import AIResponse


class BaseProvider(ABC):
    """Base class for AI providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate AI response"""
        pass

    @abstractmethod
    async def list_models(self) -> List[str]:
        """List available models"""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider resources"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        pass
