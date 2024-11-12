"""Metrics configuration"""

from dataclasses import dataclass
from typing import Callable, List, Optional

from pepperpy.core.config import ModuleConfig

from .types import MetricEvent


@dataclass
class MetricsConfig(ModuleConfig):
    """Configuration for metrics collection"""

    storage_backend: str = "memory"  # memory, file, custom
    file_path: Optional[str] = None
    custom_handler: Optional[Callable[[List[MetricEvent]], None]] = None
    auto_flush_enabled: bool = True
    flush_interval: int = 60  # seconds
    flush_threshold: int = 100  # events
    include_metadata: bool = True
