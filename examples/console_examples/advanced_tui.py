import asyncio

from textual.app import App
from textual.widgets import Footer, Header, Static

from pepperpy.console import ConsoleModule
from pepperpy.console.tui.forms import Form, FormField
from pepperpy.console.tui.layouts import DashboardLayout, SidebarLayout, TabLayout
from pepperpy.console.tui.widgets import SmartTable
from pepperpy.core import Application


class AdvancedTUI(App):
    """Advanced TUI application"""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_sidebar", "Toggle Sidebar"),
        ("1-3", "switch_tab", "Switch Tab"),
    ]

    def __init__(self, console_module: ConsoleModule):
        super().__init__()
        self.console = console_module

    def compose(self):
        """Create application layout"""
        yield Header()

        # Create main layout with sidebar
        layout = SidebarLayout()

        # Add navigation to sidebar
        nav_items = ["Dashboard", "Forms", "Tables"]
        for item in nav_items:
            layout.add_to_sidebar(Static(item))

        # Create tab layout for main content
        tabs = TabLayout()

        # Add dashboard tab
        dashboard = DashboardLayout(columns=2)
        dashboard.add_widget(
            self._create_stats_widget(), title="Statistics", span={"column": 2}
        )
        dashboard.add_widget(self._create_chart_widget(), title="Chart")
        dashboard.add_widget(self._create_list_widget(), title="Recent Items")
        tabs.add_tab("Dashboard", dashboard)

        # Add form tab
        form = Form(
            [
                FormField(name="name", label="Name", required=True),
                FormField(name="email", label="Email", validator=self._validate_email),
                FormField(
                    name="role",
                    label="Role",
                    type="select",
                    choices=["Admin", "User", "Guest"],
                ),
            ]
        )
        tabs.add_tab("Forms", form)

        # Add table tab
        table = SmartTable(sortable=True, filterable=True)
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Status")
        # Add sample data
        for i in range(10):
            table.add_row(str(i), f"Item {i}", "Active")
        tabs.add_tab("Tables", table)

        # Add tabs to layout
        layout.add_to_content(tabs)

        yield layout
        yield Footer()

    def _validate_email(self, value: str) -> bool:
        """Validate email format"""
        return "@" in value and "." in value

    def action_toggle_sidebar(self) -> None:
        """Toggle sidebar visibility"""
        self.query_one(SidebarLayout).toggle_sidebar()

    def action_switch_tab(self, tab: int) -> None:
        """Switch to tab by number"""
        tabs = self.query_one(TabLayout)
        if 1 <= tab <= len(tabs.tabs):
            tabs.switch_tab(list(tabs.tabs.keys())[tab - 1])


async def main():
    # Create application
    app = Application()

    # Configure console module
    console = (
        ConsoleModule.create()
        .configure(theme={"info": "cyan", "success": "green bold", "error": "red bold"})
        .build()
    )

    app.add_module(console)

    # Run TUI
    tui = AdvancedTUI(console)
    await tui.run_async()


if __name__ == "__main__":
    asyncio.run(main())
