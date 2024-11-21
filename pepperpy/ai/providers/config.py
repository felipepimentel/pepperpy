"""AI provider configuration"""

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class AIConfig(BaseModel):
    """AI configuration"""

    provider: str
    api_key: str
    model: str = Field(default="gpt-3.5-turbo")
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=2048, gt=0)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True

    @classmethod
    def get_default(cls) -> "AIConfig":
        """Get default configuration"""
        return cls(
            provider="openai",
            api_key="dummy",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=2048,
        )
