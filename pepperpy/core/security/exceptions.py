"""Security specific exceptions"""

from pepperpy.core.exceptions import CoreError


class SecurityError(CoreError):
    """Base exception for security errors"""

    pass


class AuthError(SecurityError):
    """Authentication error"""

    pass


class PermissionError(SecurityError):
    """Permission denied error"""

    pass


class RoleError(SecurityError):
    """Role validation error"""

    pass


class TokenError(SecurityError):
    """Token validation error"""

    pass


class ConfigError(SecurityError):
    """Security configuration error"""

    pass
