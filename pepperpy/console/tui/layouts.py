from typing import Any, Dict, Optional

from rich.text import Text
from textual.containers import Container, Grid, Horizontal
from textual.reactive import reactive
from textual.widgets import Static


class DashboardLayout(Container):
    """Responsive dashboard layout"""

    def __init__(self, columns: int = 3) -> None:
        super().__init__()
        self.columns = columns
        self.grid = Grid()
        self.grid.styles.grid_size_columns = columns

    def add_widget(
        self,
        widget: Any,
        title: Optional[str] = None,
        span: Optional[Dict[str, int]] = None,
    ) -> None:
        """Add widget to dashboard"""
        container = Container()

        if title:
            title_widget = Static(Text(title, style="bold"))
            container.mount(title_widget)

        container.mount(widget)

        if span:
            container.styles.grid_column_span = span.get("column", 1)
            container.styles.grid_row_span = span.get("row", 1)

        self.grid.mount(container)


class SidebarLayout(Horizontal):
    """Layout with collapsible sidebar"""

    collapsed = reactive(False)

    def __init__(self, sidebar_width: int = 30) -> None:
        super().__init__()
        self.sidebar_width = sidebar_width
        self.sidebar = Container()
        self.content = Container()

        self.mount(self.sidebar)
        self.mount(self.content)

    def toggle_sidebar(self) -> None:
        """Toggle sidebar visibility"""
        self.collapsed = not self.collapsed
        self.sidebar.styles.width = 0 if self.collapsed else self.sidebar_width

    def add_to_sidebar(self, widget: Any) -> None:
        """Add widget to sidebar"""
        self.sidebar.mount(widget)

    def add_to_content(self, widget: Any) -> None:
        """Add widget to main content"""
        self.content.mount(widget)


class TabLayout(Container):
    """Multi-tab layout"""

    def __init__(self) -> None:
        super().__init__()
        self.tabs: Dict[str, Container] = {}
        self.current_tab: Optional[str] = None
        self.tab_bar = Horizontal()
        self.content = Container()

        self.mount(self.tab_bar)
        self.mount(self.content)

    def add_tab(self, name: str, widget: Any) -> None:
        """Add new tab"""
        # Create tab button
        tab_button = Static(name)
        tab_button.styles.padding = (1, 2)
        tab_button.styles.border = ("solid", "white")

        # Create tab content
        tab_content = Container()
        tab_content.mount(widget)
        tab_content.styles.display = "none"

        self.tabs[name] = tab_content
        self.tab_bar.mount(tab_button)
        self.content.mount(tab_content)

        if not self.current_tab:
            self.switch_tab(name)

    def switch_tab(self, name: str) -> None:
        """Switch to tab"""
        if name not in self.tabs:
            return

        if self.current_tab:
            self.tabs[self.current_tab].styles.display = "none"

        self.tabs[name].styles.display = "block"
        self.current_tab = name
