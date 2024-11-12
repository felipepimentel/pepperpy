"""Cache specific exceptions"""

from pepperpy.core.exceptions import CoreError


class CacheError(CoreError):
    """Base exception for cache errors"""

    pass


class CacheKeyError(CacheError):
    """Error for invalid cache key operations"""

    pass


class CacheValueError(CacheError):
    """Error for invalid cache value operations"""

    pass
