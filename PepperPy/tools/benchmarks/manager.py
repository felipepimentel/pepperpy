"""Benchmark management utilities."""

import json
import toml
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypedDict, NotRequired

from .base import BenchmarkBase


class RegressionInfo(TypedDict):
    """Regression information."""

    metric: str
    current: float
    baseline: float
    regression: float


class ComparisonResult(TypedDict):
    """Benchmark comparison result."""

    current: dict[str, Any]
    baseline: NotRequired[dict[str, Any]]
    regressions: NotRequired[dict[str, RegressionInfo]]


class BenchmarkManager:
    """Manages benchmark execution and results."""

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize benchmark manager."""
        self.config = self._load_config(config_path)
        output_dir = Path(self.config["output_dir"])
        self.base = BenchmarkBase(output_dir=output_dir)

    def _load_config(self, config_path: Path | None = None) -> dict[str, Any]:
        """Load benchmark configuration."""
        default_config = Path("tools/config/benchmark.toml")
        config_file = config_path or default_config

        if not config_file.exists():
            return {
                "output_dir": "benchmark_results",
                "compare_to": "main",
                "thresholds": {"mean": 1.2, "median": 1.1, "max": 1.5},
            }

        return toml.load(config_file)["tool"]["benchmark"]

    def compare_results(self, current: Path, baseline: Path | None = None) -> ComparisonResult:
        """Compare benchmark results.

        Args:
            current: Path to current benchmark results
            baseline: Optional path to baseline benchmark results

        Returns:
            Dictionary containing comparison results
        """
        with open(current) as f:
            current_data = json.load(f)

        if not baseline:
            return {"current": current_data}

        with open(baseline) as f:
            baseline_data = json.load(f)

        return {
            "current": current_data,
            "baseline": baseline_data,
            "regressions": self._check_regressions(current_data, baseline_data),
        }

    def _check_regressions(
        self, current: dict[str, Any], baseline: dict[str, Any]
    ) -> dict[str, RegressionInfo]:
        """Check for performance regressions.

        Args:
            current: Current benchmark results
            baseline: Baseline benchmark results

        Returns:
            Dictionary mapping benchmark names to regression details
        """
        regressions: dict[str, RegressionInfo] = {}
        thresholds = self.config["thresholds"]

        for benchmark in current["benchmarks"]:
            name = benchmark["name"]
            if name not in baseline["benchmarks"]:
                continue

            baseline_stats = baseline["benchmarks"][name]

            for metric, threshold in thresholds.items():
                if benchmark[metric] > baseline_stats[metric] * threshold:
                    regressions[name] = {
                        "metric": metric,
                        "current": benchmark[metric],
                        "baseline": baseline_stats[metric],
                        "regression": benchmark[metric] / baseline_stats[metric],
                    }

        return regressions 