"""Common type definitions for AI module."""
from typing import TypeVar, Protocol, Dict, Any, List, Optional
from dataclasses import dataclass, field
import numpy as np

# Generic types
T = TypeVar('T')
ModelID = str
ProviderID = str

# Protocol definitions
class VectorOperation(Protocol):
    """Protocol for vector operations."""
    def similarity(self, a: np.ndarray, b: np.ndarray) -> float: ...
    def combine(self, vectors: List[np.ndarray]) -> np.ndarray: ...

class TokenCounter(Protocol):
    """Protocol for token counting."""
    def count(self, text: str) -> int: ...
    def count_batch(self, texts: List[str]) -> List[int]: ...

# Common dataclasses
@dataclass
class AIResource:
    """Base class for AI resources."""
    id: str
    name: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

@dataclass
class ModelCapabilities:
    """Defines what a model can do."""
    supports_streaming: bool = False
    supports_functions: bool = False
    supports_vision: bool = False
    supports_audio: bool = False
    max_context_length: Optional[int] = None
    max_output_length: Optional[int] = None