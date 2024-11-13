"""Mock utilities for testing"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

T = TypeVar("T")
MockFunction = Callable[..., Any]
MockReturn = Union[Any, Exception]


@dataclass
class MockCall:
    """Mock function call record"""

    args: tuple
    kwargs: Dict[str, Any]
    return_value: Any
    exception: Optional[Exception] = None


@dataclass
class Mock:
    """Mock function or object"""

    name: str
    return_value: Any = None
    side_effect: Optional[Union[Exception, MockFunction]] = None
    calls: List[MockCall] = field(default_factory=list)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Handle mock function call"""
        if self.side_effect is not None:
            if isinstance(self.side_effect, Exception):
                self.calls.append(MockCall(args, kwargs, None, self.side_effect))
                raise self.side_effect
            result = self.side_effect(*args, **kwargs)
        else:
            result = self.return_value

        self.calls.append(MockCall(args, kwargs, result))
        return result

    def reset(self) -> None:
        """Reset mock call history"""
        self.calls.clear()


def create_mock(
    name: str,
    return_value: Any = None,
    side_effect: Optional[Union[Exception, MockFunction]] = None,
) -> Mock:
    """Create a mock function

    Args:
        name: Mock name
        return_value: Value to return when called
        side_effect: Exception to raise or function to call

    Returns:
        Mock: Mock function
    """
    return Mock(name=name, return_value=return_value, side_effect=side_effect)
