"""Security decorators"""

import functools
from typing import Any, Callable, TypeVar, cast

from .context_manager import get_security_context
from .exceptions import SecurityError

T = TypeVar("T", bound=Callable[..., Any])


def require_auth(func: T) -> T:
    """Require authentication decorator"""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        context = get_security_context()
        if not context:
            raise SecurityError("Authentication required")
        return await func(*args, **kwargs)

    return cast(T, wrapper)


def require_roles(*roles: str) -> Callable[[T], T]:
    """Require roles decorator"""

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = get_security_context()
            if not context:
                raise SecurityError("Authentication required")
            if not any(role in context.roles for role in roles):
                raise SecurityError(f"Required roles: {roles}")
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def require_permissions(*permissions: str) -> Callable[[T], T]:
    """Require permissions decorator"""

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = get_security_context()
            if not context:
                raise SecurityError("Authentication required")
            if not all(perm in context.permissions for perm in permissions):
                raise SecurityError(f"Required permissions: {permissions}")
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def require_active(func: T) -> T:
    """Require active user decorator"""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        context = get_security_context()
        if not context:
            raise SecurityError("Authentication required")
        if not context.active:
            raise SecurityError("User account is not active")
        return await func(*args, **kwargs)

    return cast(T, wrapper)
