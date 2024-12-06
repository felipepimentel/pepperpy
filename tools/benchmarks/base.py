"""Base benchmark utilities"""
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

# Importar pytest como opcional para evitar erro de resolução
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

import json
from pathlib import Path

P = ParamSpec("P")
R = TypeVar("R")

class BenchmarkBase:
    """Base class for benchmarks"""
    
    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or Path("benchmark_results")
        self.output_dir.mkdir(exist_ok=True)
        
    def save_results(self, name: str, results: dict[str, Any]) -> None:
        """Save benchmark results"""
        output_file = self.output_dir / f"{name}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

    @staticmethod
    def benchmark(func: Callable[P, R]) -> Callable[P, R]:
        """Decorator for benchmark functions"""
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not PYTEST_AVAILABLE:
                return func(*args, **kwargs)
            return pytest.mark.benchmark(func)(*args, **kwargs)  # type: ignore
        return wrapper 