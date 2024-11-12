"""Metrics specific exceptions"""

from pepperpy.core.exceptions import CoreError


class MetricsError(CoreError):
    """Base exception for metrics errors"""

    pass


class MetricsStorageError(MetricsError):
    """Error during metrics storage operation"""

    pass


class MetricsFlushError(MetricsError):
    """Error during metrics flush operation"""

    pass
