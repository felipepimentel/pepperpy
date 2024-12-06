"""Code metrics types."""

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass
class ComplexityMetrics:
    """Code complexity metrics."""

    cognitive_complexity: float
    cyclomatic_complexity: float
    halstead_difficulty: float
    halstead_effort: float
    halstead_volume: float
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class CoverageMetrics:
    """Code coverage metrics."""

    line_coverage: float
    branch_coverage: float
    statement_coverage: float
    total_lines: int
    covered_lines: int
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TestCoverageMetrics:
    """Test coverage metrics."""

    test_coverage: float
    test_count: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class QualityMetrics:
    """Code quality metrics."""

    maintainability_index: float
    quality_score: float
    bug_risk: float
    duplication_rate: float
    documentation_rate: float
    metadata: JsonDict = field(default_factory=dict)
