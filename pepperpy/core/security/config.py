"""Security configuration"""

from dataclasses import dataclass, field
from typing import Dict

from pepperpy.core.config import ModuleConfig


@dataclass
class SecurityConfig(ModuleConfig):
    """Configuration for security"""

    secret_key: str
    token_expiry: int = 3600  # 1 hour
    password_min_length: int = 8
    password_require_special: bool = True
    password_require_numbers: bool = True
    max_login_attempts: int = 3
    lockout_duration: int = 300  # 5 minutes
    session_timeout: int = 1800  # 30 minutes
    allow_multiple_sessions: bool = True
    metadata: Dict[str, str] = field(default_factory=dict)
