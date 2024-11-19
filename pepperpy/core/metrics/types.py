"""Metrics type definitions"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class MetricType(Enum):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class Metric:
    """Metric data"""
    name: str
    type: MetricType
    value: float
    timestamp: datetime
    tags: dict[str, str]
    metadata: dict[str, Any]


MetricValue = int | float 