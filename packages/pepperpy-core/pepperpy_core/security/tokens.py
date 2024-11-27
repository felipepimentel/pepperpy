"""Security token implementation"""

from dataclasses import dataclass, field
from datetime import datetime

from ..base.types import JsonDict
from ..utils.datetime import utc_now


@dataclass
class SecurityToken:
    """Security token"""

    token: str
    expires_at: datetime
    user_id: str
    metadata: JsonDict = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        """Check if token is expired"""
        now = utc_now()
        if self.expires_at.tzinfo is None:
            # Convert naive to aware
            expires_at = self.expires_at.replace(tzinfo=now.tzinfo)
        else:
            expires_at = self.expires_at
        return now > expires_at


__all__ = [
    "SecurityToken",
]
