"""Security type definitions"""

from dataclasses import dataclass, field
from datetime import datetime

from pepperpy.core.types import JsonDict


@dataclass
class Permission:
    """Permission definition"""

    name: str
    description: str
    scope: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class Role:
    """Role definition"""

    name: str
    description: str
    permissions: set[str]
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class User:
    """User information"""

    id: str
    username: str
    email: str | None = None
    roles: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=set)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: datetime | None = None
    active: bool = True


@dataclass
class AuthToken:
    """Authentication token"""

    token: str
    type: str = "bearer"
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AuthContext:
    """Authentication context"""

    user_id: str | None = None
    roles: list[str] = field(default_factory=list)
    permissions: set[str] = field(default_factory=set)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: datetime | None = None
    active: bool = True
