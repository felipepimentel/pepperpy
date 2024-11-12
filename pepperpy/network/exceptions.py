"""Network exceptions"""

from typing import Optional

from pepperpy.core.exceptions import CoreError


class NetworkError(CoreError):
    """Base network error"""

    def __init__(
        self, message: str, status_code: Optional[int] = None, cause: Optional[Exception] = None
    ) -> None:
        super().__init__(message, cause)
        self.status_code = status_code


class ConnectionError(NetworkError):
    """Connection establishment error"""

    pass


class TimeoutError(NetworkError):
    """Request timeout error"""

    pass


class WebSocketError(NetworkError):
    """WebSocket specific error"""

    pass
