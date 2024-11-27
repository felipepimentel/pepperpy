"""PepperPy Core Framework

Core functionality and base classes for the PepperPy framework.
"""

from .base import (
    BaseModule,
    JsonDict,
    JsonValue,
    ModuleId,
    ResourceId,
)
from .cache import BaseCache, MemoryCache
from .config import ConfigManager, Settings
from .logging import LogConfig, StructuredLogger
from .metrics import Metric, MetricsCollector
from .tasks import Task, TaskManager, TaskStatus
from .validation import ValidationLevel, ValidationPipeline, ValidationResult, Validator

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Base
    "BaseModule",
    "JsonDict",
    "JsonValue",
    "ModuleId",
    "ResourceId",
    # Cache
    "BaseCache",
    "MemoryCache",
    # Config
    "ConfigManager",
    "Settings",
    # Logging
    "LogConfig",
    "StructuredLogger",
    # Metrics
    "Metric",
    "MetricsCollector",
    # Tasks
    "Task",
    "TaskManager",
    "TaskStatus",
    # Validation
    "ValidationLevel",
    "ValidationPipeline",
    "ValidationResult",
    "Validator",
]
