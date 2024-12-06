"""Benchmark management utilities"""

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import toml

from .base import BenchmarkBase


class BenchmarkManager:
    """Manages benchmark execution and results"""

    def __init__(self, config_path: Path | None = None) -> None:
        self.config = self._load_config(config_path)
        self.base = BenchmarkBase(Path(self.config["output_dir"]))

    def _load_config(self, config_path: Path | None = None) -> dict[str, Any]:
        """Load benchmark configuration"""
        default_config = Path("tools/config/benchmark.toml")
        config_file = config_path or default_config

        if not config_file.exists():
            return {
                "output_dir": "benchmark_results",
                "compare_to": "main",
                "thresholds": {"mean": 1.2, "median": 1.1, "max": 1.5},
            }

        return toml.load(config_file)["tool"]["benchmark"]

    def run_benchmarks(
        self, packages: Sequence[str] | None = None, markers: Sequence[str] | None = None
    ) -> None:
        """Run benchmarks for specified packages"""
        import pytest

        packages = packages or [p.name for p in Path("packages").iterdir() if p.is_dir()]

        for package in packages:
            args = ["--benchmark-only"]
            if markers:
                args.extend(["-m", " or ".join(markers)])

            try:
                pytest.main(args, plugins=["pytest-benchmark"])
            except Exception as e:
                print(f"Benchmark failed for {package}: {e}")

    def compare_results(self, current: Path, baseline: Path | None = None) -> dict[str, Any]:
        """Compare benchmark results"""
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
    ) -> dict[str, Any]:
        """Check for performance regressions"""
        regressions = {}
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
