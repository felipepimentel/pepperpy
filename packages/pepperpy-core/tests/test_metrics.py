"""Test metrics functionality."""

import pytest

from pepperpy_core.telemetry.config import TelemetryConfig
from pepperpy_core.telemetry.metrics import MetricsCollector


@pytest.fixture
def metrics_config() -> TelemetryConfig:
    """Create metrics configuration.

    Returns:
        Metrics configuration
    """
    return TelemetryConfig(
        name="test-metrics",
        enabled=True,
        buffer_size=1000,
        flush_interval=60.0,
    )


@pytest.fixture
async def metrics_collector(metrics_config: TelemetryConfig) -> MetricsCollector:
    """Create metrics collector.

    Args:
        metrics_config: Metrics configuration

    Returns:
        Initialized metrics collector
    """
    collector = MetricsCollector()
    collector.config = metrics_config  # Substituir a configuração padrão
    await collector.initialize()
    return collector


@pytest.mark.asyncio
async def test_record_metric(metrics_collector: MetricsCollector) -> None:
    """Test recording metrics."""
    await metrics_collector.collect(
        name="test_metric",
        value=1.0,
        tags={"test": "true"},
    )

    stats = await metrics_collector.get_stats()
    assert stats["total_metrics"] == 1
    assert "test_metric" in stats["metric_names"]
    assert stats["enabled"] is True


@pytest.mark.asyncio
async def test_record_multiple_metrics(metrics_collector: MetricsCollector) -> None:
    """Test recording multiple metrics."""
    test_metrics = [
        ("metric1", 1.0, {"tag": "1"}),
        ("metric2", 2.0, {"tag": "2"}),
    ]

    for name, value, tags in test_metrics:
        await metrics_collector.collect(
            name=name,
            value=value,
            tags=tags,
        )

    stats = await metrics_collector.get_stats()
    assert stats["total_metrics"] == len(test_metrics)
    for name, _, _ in test_metrics:
        assert name in stats["metric_names"]


@pytest.mark.asyncio
async def test_cleanup(metrics_collector: MetricsCollector) -> None:
    """Test metrics cleanup."""
    await metrics_collector.collect(
        name="test",
        value=1.0,
    )
    await metrics_collector.cleanup()

    stats = await metrics_collector.get_stats()
    assert stats["total_metrics"] == 0
