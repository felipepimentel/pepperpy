"""Core interfaces for Pepperpy components."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic

T = TypeVar('T')
R = TypeVar('R')

class PepperpyComponent(ABC):
    """Base interface for all Pepperpy components."""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize component resources."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup component resources."""
        pass
    
    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """Check if component is ready."""
        pass

class ProcessorComponent(PepperpyComponent, Generic[T, R]):
    """Base interface for components that process data."""
    
    @abstractmethod
    async def process(self, input_data: T) -> R:
        """Process input data and return result."""
        pass
    
    @abstractmethod
    async def validate(self, input_data: T) -> bool:
        """Validate input data before processing."""
        pass

class StateManageable(ABC):
    """Interface for components with state management."""
    
    @abstractmethod
    async def save_state(self) -> Dict[str, Any]:
        """Save component state."""
        pass
    
    @abstractmethod
    async def load_state(self, state: Dict[str, Any]) -> None:
        """Load component state."""
        pass
    
    @abstractmethod
    async def reset_state(self) -> None:
        """Reset component state."""
        pass

class Observable(ABC):
    """Interface for observable components."""
    
    @abstractmethod
    def subscribe(self, event_type: str, handler: callable) -> None:
        """Subscribe to component events."""
        pass
    
    @abstractmethod
    def unsubscribe(self, event_type: str, handler: callable) -> None:
        """Unsubscribe from component events."""
        pass