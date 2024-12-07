"""Base benchmark functionality."""

from pathlib import Path
import json


class BenchmarkBase:
    """Base class for benchmarks."""

    def __init__(self, output_dir: Path | None = None) -> None:
        """Initialize benchmark base.

        Args:
            output_dir: Optional output directory for benchmark results
        """
        self.output_dir = output_dir or Path("benchmark_results")
        self.output_dir.mkdir(exist_ok=True)

    def save_results(self, name: str, results: dict) -> None:
        """Save benchmark results.

        Args:
            name: Benchmark name
            results: Benchmark results
        """
        output_file = self.output_dir / f"{name}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)


__all__ = ["BenchmarkBase"]
