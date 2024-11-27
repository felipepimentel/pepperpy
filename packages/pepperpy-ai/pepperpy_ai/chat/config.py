"""Chat configuration"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict

from bko.core.exceptions import ConfigError


@dataclass
class ChatConfig:
    """Chat configuration"""

    model: str
    temperature: float = 0.7
    max_tokens: int = 2048
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Constants
    MIN_TEMPERATURE: ClassVar[float] = 0.0
    MAX_TEMPERATURE: ClassVar[float] = 1.0
    MIN_TOKENS: ClassVar[int] = 1

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not self.model:
            raise ValueError("Model name cannot be empty")

        if not self.MIN_TEMPERATURE <= self.temperature <= self.MAX_TEMPERATURE:
            raise ValueError(
                f"Temperature must be between {self.MIN_TEMPERATURE} and {self.MAX_TEMPERATURE}"
            )

        if self.max_tokens < self.MIN_TOKENS:
            raise ValueError(f"Max tokens must be at least {self.MIN_TOKENS}")

    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update metadata.

        Args:
            metadata: New metadata
        """
        self.metadata = metadata

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatConfig":
        """Create from dictionary.

        Args:
            data: Configuration dictionary

        Returns:
            ChatConfig: Configuration instance

        Raises:
            ConfigError: If dictionary is invalid
        """
        try:
            return cls(**data)
        except (ValueError, TypeError) as e:
            raise ConfigError(f"Invalid configuration: {e}")

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return (
            f"ChatConfig(model={self.model}, temperature={self.temperature}, "
            f"max_tokens={self.max_tokens}, metadata={self.metadata})"
        )
