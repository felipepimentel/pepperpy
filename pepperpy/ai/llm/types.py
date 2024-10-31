"""Type definitions and common structures for LLM module."""
from typing import TypedDict, Literal, Union, Dict, List, Optional, Protocol, Any
from dataclasses import dataclass, field

Role = Literal["system", "user", "assistant"]

class Message(TypedDict):
    """Represents a chat message."""
    role: Role
    content: str

@dataclass(frozen=True)
class ModelInfo:
    """Information about an LLM model."""
    name: str
    provider: str
    context_window: int
    input_cost_per_1k: float
    output_cost_per_1k: float
    supports_functions: bool = False
    max_tokens: Optional[int] = None

class PromptProcessor(Protocol):
    """Protocol for prompt processing functions."""
    def __call__(self, content: str) -> str: ...

@dataclass
class Conversation:
    """Represents an ongoing conversation."""
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None

    def add_message(self, role: Role, content: str) -> None:
        """Add a message to the conversation."""
        self.messages.append({"role": role, "content": content})

    def get_context(self) -> List[Message]:
        """Get the current conversation context."""
        return self.messages.copy() 