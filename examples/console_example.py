import asyncio
import signal
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pepperpy.console import Console, ConsoleTemplates, Style
from pepperpy.console.components import Layout, WizardStep


async def demo_rich_text(console: Console) -> None:
    """Demonstrate rich text formatting capabilities"""
    console.title("Rich Text Formatting Demo")

    # Markdown
    console.markdown(
        """
    # Rich Markdown Support
    - **Bold text** and *italic text*
    - Code blocks with syntax highlighting
    - [Links](https://example.com)
    """
    )

    # Syntax highlighting
    code = """
    def hello_world():
        print("Hello, World!")
    """
    console.syntax(code, "python")

    # Panels
    console.panel(
        content="Important information in a panel",
        title="System Notice",
        style=Style.HIGHLIGHT,
        border_style=Style.INFO,
        padding=(1, 3),
    )

    console.divider()


async def demo_layout(console: Console) -> None:
    """Demonstrate layout capabilities"""
    console.title("Layout Demo")

    layout = Layout()

    # Criar seções do layout
    layout.split(direction="vertical", sections=["header", "body", "footer"])

    layout.add_panel(section="header", content="System Dashboard", style=Style.HIGHLIGHT)

    # Dividir a seção body
    layout.split_section("body", direction="horizontal", sections=["stats", "chart"])

    # Adicionar conteúdo às seções
    stats = {"Users": 1234, "Active": 789, "CPU": "23%", "Memory": "45%"}

    layout.add_stats(section="stats", data=stats, title="System Statistics")

    layout.add_chart(section="chart", data={"Usage": [45, 67, 89, 34, 56]}, title="Resource Usage")

    layout.add_panel(
        section="footer",
        content="Status: Online | Last Update: 2024-03-15 10:30:00",
        style=Style.INFO,
    )

    layout.render()
    console.divider()


async def demo_tree_view(console: Console) -> None:
    """Demonstrate tree view for hierarchical data"""
    console.title("Tree View Demo")

    project_structure = {
        "src": {"main.py": None, "utils": {"helpers.py": None, "config.py": None}},
        "tests": {"test_main.py": None, "test_utils.py": None},
        "docs": ["README.md", "API.md"],
    }

    console.tree(data=project_structure, title="Project Structure", style=Style.CODE)
    console.divider()


async def demo_wizard(console: Console) -> None:
    """Demonstrate configuration wizard"""
    console.title("Configuration Wizard Demo")

    steps = [
        WizardStep(
            name="project_name",
            prompt="Enter project name",
            required=True,
            validator=lambda x: len(x) >= 3,
        ),
        WizardStep(
            name="version", prompt="Enter version", default="0.1.0", pattern=r"^\d+\.\d+\.\d+$"
        ),
        WizardStep(
            name="database",
            prompt="Select database",
            choices=["SQLite", "PostgreSQL", "MySQL"],
            default="SQLite",
        ),
        WizardStep(
            name="features",
            prompt="Select features",
            multiple=True,
            choices=["api", "auth", "cache", "admin"],
            default=["api"],
        ),
    ]

    config = await console.wizard(title="Project Configuration", steps=steps, style=Style.HIGHLIGHT)

    console.info("Configuration complete:")
    console.show(config)
    console.divider()


async def demo_live_updates(console: Console) -> None:
    """Demonstrate live-updating display"""
    console.title("Live Updates Demo")

    with console.live_display() as display:
        for i in range(10):
            display.update(
                content=f"Processing... Step {i+1}/10", title="Processing", style=Style.INFO.value
            )
            await asyncio.sleep(0.5)

    console.success("Live update complete!")
    console.divider()


async def demo_chat_interface(console: Console) -> None:
    """Demonstrate chat interface"""
    console.title("Chat Interface Demo")

    chat = console.create_chat(title="Support Chat", theme="dark")

    await chat.add_message(
        content="Hello! How can I help you?", sender="assistant", style=Style.INFO
    )
    await asyncio.sleep(1)

    await chat.add_message(content="I need help with Python", sender="user", style=Style.HIGHLIGHT)
    await asyncio.sleep(1)

    await chat.add_message(
        content="What specific topic would you like to learn about?",
        sender="assistant",
        style=Style.INFO,
    )
    await asyncio.sleep(1)

    await chat.add_message(
        content="Let's start with async/await", sender="user", style=Style.HIGHLIGHT
    )

    console.divider()


async def demo_menu(console: Console) -> None:
    """Demonstrate interactive menu"""
    console.title("Interactive Menu Demo")

    menu = console.create_menu(title="Main Menu", style=Style.HIGHLIGHT)

    menu.add_item("View Status", lambda: console.info("System status: Online"))

    menu.add_item("Configure", lambda: console.info("Opening configuration..."))

    menu.add_separator()

    menu.add_item("Exit", lambda: console.warning("Exiting..."))

    await menu.show()
    console.divider()


class DemoRunner:
    """Demo runner with proper signal handling"""

    def __init__(self):
        self.console = Console()
        self._running = True

    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self._handle_signal)

    def _handle_signal(self, signum: int, frame: Optional[Any]) -> None:
        """Handle interrupt signals."""
        self._running = False
        self.console.warning("\nShutting down gracefully...")

    async def run_demo(self, name: str, demo_func) -> None:
        """Run a single demo with error handling."""
        try:
            self.console.log(ConsoleTemplates.get("demo_start", demo_name=name))
            await demo_func(self.console)
            self.console.log(ConsoleTemplates.get("demo_end", demo_name=name))

            if self._running:
                with suppress(asyncio.CancelledError):
                    await asyncio.sleep(1)

        except Exception as e:
            self.console.error(f"Error in {name} demo: {str(e)}")

    async def run(self) -> None:
        """Run all demos with proper cleanup."""
        try:
            self._setup_signal_handlers()

            # Setup
            ConsoleTemplates.add("demo_start", "[bold blue]Starting $demo_name demonstration...[/]")
            ConsoleTemplates.add("demo_end", "[bold green]Completed $demo_name demonstration[/]")

            self.console.clear()
            self.console.header(
                title="PepperPy Enhanced Console Demonstration",
                subtitle="Interactive Terminal User Interface Demo",
                style=Style.HIGHLIGHT,
            )

            # Define demos
            demos = [
                ("Rich Text", demo_rich_text),
                ("Layout", demo_layout),
                ("Tree View", demo_tree_view),
                ("Configuration Wizard", demo_wizard),
                ("Live Updates", demo_live_updates),
                ("Chat Interface", demo_chat_interface),
                ("Interactive Menu", demo_menu),
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
            self.console.error(f"Demo runner error: {str(e)}")
        finally:
            if not self._running:
                self.console.print("\n[yellow]Demo runner stopped by user[/]")


if __name__ == "__main__":
    runner = DemoRunner()
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        pass  # Runner already handles the shutdown
