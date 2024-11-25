"""AI configuration module"""

from typing import Any, ClassVar, Dict, Type, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar('T', bound='AIConfig')


class AIConfig(BaseModel):
    """Base configuration for AI components"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Component name")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    _default_instance: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def get_default(cls: Type[T]) -> T:
        """Get default configuration instance"""
        if cls.__name__ not in cls._default_instance:
            cls._default_instance[cls.__name__] = cls(name="default")
        return cls._default_instance[cls.__name__]

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump(*args, **kwargs)
