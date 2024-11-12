from dataclasses import dataclass
from typing import Optional


@dataclass
class AIConfig:
    """AI module configuration"""

    provider: str = "mock"
    api_key: Optional[str] = None
    model: str = "default"
