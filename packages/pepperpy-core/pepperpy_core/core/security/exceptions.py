"""Security-related exceptions"""

from bko.core.exceptions import PepperPyError


class SecurityError(PepperPyError):
    """Base security error"""


class AuthError(SecurityError):
    """Authentication error"""


class PermissionError(SecurityError):
    """Permission error"""


class TokenError(SecurityError):
    """Token error"""


class CryptoError(SecurityError):
    """Cryptography error"""
