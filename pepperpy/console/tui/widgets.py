from typing import Callable, List, Optional

from rich.text import Text
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import DataTable, Input, Static


class SmartInput(Input):
    """Enhanced input with validation and completion"""

    class Changed(Message):
        """Input changed message"""

        def __init__(self, value: str, valid: bool) -> None:
            self.value = value
            self.valid = valid
            super().__init__()

    def __init__(
        self,
        validator: Optional[Callable[[str], bool]] = None,
        completer: Optional[Callable[[str], List[str]]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.validator = validator
        self.completer = completer

    def on_input_changed(self, value: str) -> None:
        """Handle input changes"""
        valid = True if not self.validator else self.validator(value)
        self.post_message(self.Changed(value, valid))

        if self.completer:
            completions = self.completer(value)
            if completions:
                # Show completion popup
                pass


class SmartTable(DataTable):
    """Enhanced table with sorting and filtering"""

    def __init__(
        self, *args, sortable: bool = True, filterable: bool = True, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.sortable = sortable
        self.filterable = filterable
        self._filter_text = ""
        self._sort_column = None
        self._sort_reverse = False

    def filter(self, text: str) -> None:
        """Filter table rows"""
        self._filter_text = text.lower()
        self._refresh_view()

    def sort(self, column: int, reverse: bool = False) -> None:
        """Sort table by column"""
        self._sort_column = column
        self._sort_reverse = reverse
        self._refresh_view()

    def _refresh_view(self) -> None:
        """Update table view"""
        # Implementation here


class Dashboard(Container):
    """Dashboard layout with cards"""

    def __init__(self) -> None:
        super().__init__()
        self.layout = Horizontal()

    def add_card(
        self, title: str, content: Widget, width: Optional[int] = None
    ) -> None:
        """Add card to dashboard"""
        card = Container()
        card.styles.width = width
        card.styles.height = "auto"
        card.styles.padding = 1
        card.styles.border = ("solid", "white")

        title_widget = Static(Text(title, style="bold"))
        card.mount(title_widget)
        card.mount(content)

        self.layout.mount(card)
