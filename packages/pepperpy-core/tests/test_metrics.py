"""Test metrics functionality"""

import asyncio
from datetime import datetime, timezone

import pytest
from pepperpy_core.metrics import (
    Metric,
    MetricsCollector,
    MetricsConfig,
    MetricType,
    timing,
)


@pytest.fixture
def collector() -> MetricsCollector:
    """Create metrics collector"""
    return MetricsCollector(
        MetricsConfig(enabled=True, prefix="test_", default_labels={"env": "test"})
    )


async def test_counter_metric(collector: MetricsCollector) -> None:
    """Test counter metric"""
    collector.counter("counter", 1.0, {"label": "value"})
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_counter"
    assert metric.type == MetricType.COUNTER
    assert metric.value == 1.0
    assert metric.labels == {"env": "test", "label": "value"}
    assert isinstance(metric.timestamp, datetime)
    assert metric.timestamp.tzinfo == timezone.utc


def test_gauge_metric(collector: MetricsCollector) -> None:
    """Test gauge metric"""
    collector.gauge("gauge", 42.0, {"label": "value"})
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_gauge"
    assert metric.type == MetricType.GAUGE
    assert metric.value == 42.0
    assert metric.labels == {"env": "test", "label": "value"}
    assert isinstance(metric.timestamp, datetime)
    assert metric.timestamp.tzinfo == timezone.utc


def test_histogram_metric(collector: MetricsCollector) -> None:
    """Test histogram metric"""
    collector.histogram("histogram", 0.5, {"label": "value"})
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_histogram"
    assert metric.type == MetricType.HISTOGRAM
    assert metric.value == 0.5
    assert metric.labels == {"env": "test", "label": "value"}
    assert isinstance(metric.timestamp, datetime)
    assert metric.timestamp.tzinfo == timezone.utc


def test_summary_metric(collector: MetricsCollector) -> None:
    """Test summary metric"""
    collector.summary("summary", 0.99, {"label": "value"})
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_summary"
    assert metric.type == MetricType.SUMMARY
    assert metric.value == 0.99
    assert metric.labels == {"env": "test", "label": "value"}
    assert isinstance(metric.timestamp, datetime)
    assert metric.timestamp.tzinfo == timezone.utc


def test_metric_prefix(collector: MetricsCollector) -> None:
    """Test metric prefix"""
    collector.counter("counter", 1.0)
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_counter"
    assert metric.type == MetricType.COUNTER
    assert metric.value == 1.0
    assert metric.labels == {"env": "test"}


def test_default_labels(collector: MetricsCollector) -> None:
    """Test default labels"""
    collector.config.default_labels = {"app": "test"}
    collector.counter("counter", labels={"custom": "value"})
    metrics = collector.collect()

    assert metrics[0].labels == {"app": "test", "custom": "value"}


def test_collector_registration(collector: MetricsCollector) -> None:
    """Test collector registration"""

    def custom_collector() -> list[Metric]:
        return [
            Metric(name="custom_metric", type=MetricType.COUNTER, value=1.0, labels={"env": "test"})
        ]

    collector.register_collector("custom", custom_collector)
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_custom_metric"
    assert metric.type == MetricType.COUNTER
    assert metric.value == 1.0
    assert metric.labels == {"env": "test"}
    assert isinstance(metric.timestamp, datetime)
    assert metric.timestamp.tzinfo == timezone.utc


def test_metrics_disabled(collector: MetricsCollector) -> None:
    """Test disabled metrics"""
    collector.config.enabled = False
    collector.counter("test", 1.0, {"label": "value"})
    metrics = collector.collect()
    assert len(metrics) == 0


def test_clear_metrics(collector: MetricsCollector) -> None:
    """Test clearing metrics"""
    collector.counter("test1", 1.0, {"label": "value1"})
    collector.counter("test2", 2.0, {"label": "value2"})
    metrics = collector.collect()
    assert len(metrics) == 2

    collector.clear()
    metrics = collector.collect()
    assert len(metrics) == 0


@pytest.mark.asyncio
async def test_timing_decorator(collector: MetricsCollector) -> None:
    """Test timing decorator"""

    class TestService:
        def __init__(self) -> None:
            self.metrics = collector

        @timing("operation")
        async def operation(self) -> None:
            await asyncio.sleep(0.1)

    service = TestService()
    await service.operation()
    metrics = collector.collect()

    assert len(metrics) == 1
    metric = metrics[0]
    assert metric.name == "test_operation_duration_seconds"
    assert metric.type == MetricType.HISTOGRAM
    assert 0.1 <= metric.value <= 0.2
    assert metric.labels == {"env": "test"}
    assert isinstance(metric.timestamp, datetime)
    assert metric.timestamp.tzinfo == timezone.utc
