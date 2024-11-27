"""Security context manager"""

from contextvars import ContextVar

from .types import AuthContext

security_context: ContextVar[AuthContext | None] = ContextVar("security_context", default=None)


def get_security_context() -> AuthContext | None:
    """Get current security context"""
    return security_context.get()


def set_security_context(context: AuthContext | None) -> None:
    """Set security context"""
    security_context.set(context)
