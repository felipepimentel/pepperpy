"""Enhanced console demonstration"""

import asyncio
import signal
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pepperpy.console import (
    Button,
    Console,
    ConsoleTemplates,
    Layout,
    Menu,
    Style,
    Table,
    Toast,
    ToastType,
    WizardStep,
)
from pepperpy.core.logging import LogConfig, LogLevel, get_logger


async def demo_rich_text(console: Console) -> None:
    """Demonstrate rich text formatting capabilities"""
    console.title("Rich Text Formatting Demo")

    # Markdown with code blocks
    console.markdown(
        """
    # Advanced Markdown Support
    
    ## Text Formatting
    - **Bold text** and *italic text*
    - ~~Strikethrough~~ and `inline code`
    - [External links](https://example.com)
    
    ## Code Examples    ```python
    async def hello_world():
        print("Hello from PepperPy!")    ```
    
    ## Lists
    1. First item
    2. Second item
       - Nested item
       - Another nested item
    """
    )

    # Syntax highlighting with line numbers
    code = """
    class DataProcessor:
        async def process(self, data: Dict[str, Any]) -> None:
            logger.info("Processing data...")
            result = await self.transform(data)
            await self.save(result)
    """
    console.syntax(code, "python", line_numbers=True)

    # Panels with rich formatting
    console.panel(
        content="[bold]Important System Notice[/]\nThis is a demonstration of advanced console features.",
        title="System Alert",
        style=Style.HIGHLIGHT,
        border_style=Style.INFO,
        padding=(1, 3),
    )

    console.divider()


async def demo_layout(console: Console) -> None:
    """Demonstrate advanced layout capabilities"""
    console.title("Advanced Layout Demo")

    layout = Layout()

    # Create complex layout structure
    layout.split(direction="vertical", sections=["header", "body", "footer"])
    layout.split_section("body", direction="horizontal", sections=["main", "sidebar"])
    layout.split_section("main", direction="vertical", sections=["stats", "chart"])
    layout.split_section("sidebar", direction="vertical", sections=["info", "controls"])

    # Header content
    layout.add_panel(
        section="header",
        content="[bold]System Dashboard[/] | Status: [green]Online[/]",
        style=Style.HIGHLIGHT,
    )

    # Stats section
    system_stats = {
        "CPU Usage": "45%",
        "Memory": "3.2GB/8GB",
        "Disk Space": "234GB/500GB",
        "Network": "125Mb/s",
        "Active Users": "1,234",
        "Response Time": "45ms",
    }
    layout.add_stats(section="stats", data=system_stats, title="System Metrics")

    # Chart section
    performance_data = {
        "CPU": [45, 42, 47, 45, 43, 44, 42],
        "Memory": [65, 63, 68, 67, 65, 66, 64],
        "Network": [25, 28, 22, 24, 26, 25, 27],
    }
    layout.add_chart(
        section="chart",
        data=performance_data,
        title="Resource Usage",
        type="line",
        labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    )

    # Info section
    layout.add_panel(
        section="info",
        content=(
            "[bold]System Information[/]\n"
            "- Version: 2.1.0\n"
            "- Last Update: 2024-03-15\n"
            "- Environment: Production\n"
            "- Region: US-West"
        ),
        style=Style.INFO,
    )

    # Controls section
    buttons = [
        Button("Refresh", lambda: console.info("Refreshing data...")),
        Button("Settings", lambda: console.info("Opening settings...")),
        Button("Help", lambda: console.info("Showing help...")),
    ]
    layout.add_component_group(section="controls", components=buttons, title="Controls")

    # Footer with status
    layout.add_panel(
        section="footer",
        content=(
            f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            "Status: [green]All Systems Operational[/]"
        ),
        style=Style.INFO,
    )

    layout.render()
    console.divider()


async def demo_interactive_components(console: Console) -> None:
    """Demonstrate interactive UI components"""
    console.title("Interactive Components Demo")

    # Create table
    columns = ["ID", "Name", "Status", "Last Updated"]
    data = [
        ["1", "Web Server", "Active", "2024-03-15 10:30"],
        ["2", "Database", "Active", "2024-03-15 10:29"],
        ["3", "Cache", "Warning", "2024-03-15 10:25"],
        ["4", "API Gateway", "Active", "2024-03-15 10:28"],
    ]

    table = Table(
        config={"x": 0, "y": 0, "width": 80, "visible": True},
        columns=columns,
        data=data,
        show_border=True,
    )
    await console.add_component(table)

    # Add toast notifications
    toast = Toast(
        config={"x": 2, "y": 10, "visible": True},
        message="System update available!",
        type=ToastType.INFO,
        duration=5.0,
    )
    await console.add_component(toast)

    # Add interactive menu
    menu = Menu(
        config={"x": 2, "y": 15, "visible": True},
        items=[
            ("View Details", lambda: console.info("Viewing details...")),
            ("Configure", lambda: console.info("Opening configuration...")),
            ("Update", lambda: console.info("Starting update...")),
            ("Exit", lambda: console.warning("Exiting...")),
        ],
    )
    await console.add_component(menu)

    console.divider()


async def demo_wizard(console: Console) -> None:
    """Demonstrate enhanced configuration wizard"""
    console.title("Advanced Configuration Wizard Demo")

    steps = [
        WizardStep(
            name="project_name",
            prompt="Enter project name",
            required=True,
            validator=lambda x: len(x) >= 3,
            help_text="Project name must be at least 3 characters long",
        ),
        WizardStep(
            name="version",
            prompt="Enter version",
            default="0.1.0",
            pattern=r"^\d+\.\d+\.\d+$",
            help_text="Version must follow semantic versioning (e.g., 1.0.0)",
        ),
        WizardStep(
            name="environment",
            prompt="Select environment",
            choices=["development", "staging", "production"],
            default="development",
            help_text="Select the deployment environment",
        ),
        WizardStep(
            name="features",
            prompt="Select features to enable",
            multiple=True,
            choices=["api", "auth", "cache", "admin", "monitoring", "notifications"],
            default=["api", "auth"],
            help_text="You can select multiple features using space",
        ),
        WizardStep(
            name="database",
            prompt="Configure database",
            type="dict",
            fields={
                "type": ("Select database type", ["postgresql", "mysql", "sqlite"]),
                "host": ("Enter database host", "localhost"),
                "port": ("Enter database port", "5432"),
            },
            help_text="Configure database connection details",
        ),
    ]

    config = await console.wizard(
        title="Project Configuration",
        steps=steps,
        style=Style.HIGHLIGHT,
        show_help=True,
    )

    console.info("Configuration complete:")
    console.show(config, title="Project Settings")
    console.divider()


class DemoRunner:
    """Enhanced demo runner with proper signal handling"""

    def __init__(self):
        # Setup logging
        log_config = LogConfig(
            name="console_demo",
            level=LogLevel.INFO,
            console_enabled=True,
            colors_enabled=True,
        )
        self.logger = get_logger("console_demo", config=log_config)
        self.console = Console()
        self._running = True

    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self._handle_signal)

    def _handle_signal(self, signum: int, frame: Optional[Any]) -> None:
        """Handle interrupt signals"""
        self._running = False
        self.console.warning("\nShutting down gracefully...")

    async def run_demo(self, name: str, demo_func) -> None:
        """Run a single demo with error handling"""
        try:
            self.logger.info(f"Starting {name} demonstration...")
            await demo_func(self.console)
            self.logger.info(f"Completed {name} demonstration")

            if self._running:
                with suppress(asyncio.CancelledError):
                    await asyncio.sleep(1)

        except Exception as e:
            self.logger.error(f"Error in {name} demo: {str(e)}")

    async def run(self) -> None:
        """Run all demos with proper cleanup"""
        try:
            self._setup_signal_handlers()

            # Setup console templates
            ConsoleTemplates.add(
                "demo_start",
                "[bold blue]Starting $demo_name demonstration...[/]",
            )
            ConsoleTemplates.add(
                "demo_end",
                "[bold green]Completed $demo_name demonstration[/]",
            )

            # Clear screen and show header
            self.console.clear()
            self.console.header(
                title="PepperPy Enhanced Console Demonstration",
                subtitle="Interactive Terminal User Interface Demo",
                style=Style.HIGHLIGHT,
            )

            # Define demos
            demos = [
                ("Rich Text", demo_rich_text),
                ("Advanced Layout", demo_layout),
                ("Interactive Components", demo_interactive_components),
                ("Configuration Wizard", demo_wizard),
            ]

            # Run demos
            for demo_name, demo_func in demos:
                if not self._running:
                    break
                await self.run_demo(demo_name, demo_func)

            # Save results if completed successfully
            if self._running:
                results = {
                    "timestamp": datetime.now().isoformat(),
                    "demos_completed": len(demos),
                    "status": "success",
                }

                output_dir = Path("demo_output")
                output_dir.mkdir(exist_ok=True)

                self.console.save_json(results, output_dir / "demo_results.json")
                self.console.success(
                    "Enhanced demo completed! Results saved to demo_output/demo_results.json"
                )

        except Exception as e:
            self.logger.error(f"Demo runner error: {str(e)}")
        finally:
            if not self._running:
                self.console.print("\n[yellow]Demo runner stopped by user[/]")


if __name__ == "__main__":
    runner = DemoRunner()
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        pass
