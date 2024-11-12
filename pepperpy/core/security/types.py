"""Security type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Set


@dataclass
class Permission:
    """Permission definition"""

    name: str
    description: str
    scope: str
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Role:
    """Role definition"""

    name: str
    description: str
    permissions: Set[str]
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class User:
    """User information"""

    id: str
    username: str
    email: Optional[str] = None
    roles: Set[str] = field(default_factory=set)
    permissions: Set[str] = field(default_factory=set)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    active: bool = True
