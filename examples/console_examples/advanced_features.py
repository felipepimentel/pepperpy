import asyncio

import typer
from rich.console import Group
from rich.syntax import Syntax

from pepperpy.console import ConsoleModule
from pepperpy.console.cli.advanced import AdvancedCLI
from pepperpy.console.cli.builder import CLIBuilder
from pepperpy.core import Application


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

    # Create CLI with advanced features
    cli = CLIBuilder(name="advanced-cli", help="Advanced CLI example", version="1.0.0")
    advanced = AdvancedCLI(cli)

    # Create command group
    config_group = advanced.group("config", help="Configuration commands")

    @config_group.command()
    @advanced.task("Loading configuration")
    @advanced.table_output(["Setting", "Value"], title="Current Configuration")
    async def show():
        """Show current configuration"""
        await asyncio.sleep(1)  # Simulate work
        return [["debug", "true"], ["log_level", "info"], ["max_retries", "3"]]

    @config_group.command()
    @advanced.task("Updating configuration")
    async def set(
        setting: str = typer.Argument(..., help="Setting name"),
        value: str = typer.Argument(..., help="Setting value"),
    ):
        """Update configuration setting"""
        # Get confirmation
        confirmed = await console.interactive.confirm(f"Update {setting} to {value}?")

        if confirmed:
            await asyncio.sleep(1)  # Simulate work
            console.success(f"Updated {setting} = {value}")

    @cli.command()
    @advanced.tree_output("Project Structure")
    async def tree():
        """Show project structure"""
        return {
            "src": {
                "main.py": None,
                "utils": ["helper.py", "config.py"],
                "data": {
                    "models": ["user.py", "product.py"],
                    "migrations": ["001_initial.py"],
                },
            },
            "tests": ["test_main.py", "test_utils.py"],
            "docs": ["README.md", "API.md"],
        }

    # Interactive features example
    @cli.command()
    async def setup():
        """Interactive setup"""
        # Select components
        components = await console.interactive.select(
            "Select components to install:",
            choices=["database", "cache", "queue", "scheduler"],
            multi=True,
        )

        # Get configuration
        workers = await console.interactive.input_number(
            "Number of workers:", minimum=1, maximum=10, default=4
        )

        # Edit configuration
        config = await console.interactive.editor(
            "Edit configuration:",
            default="debug: true\nlog_level: info",
            extension=".yaml",
        )

        # Show results
        console.print("\nSetup Summary:")
        console.print(
            console.create_panel(
                Group(
                    f"Components: {', '.join(components)}",
                    f"Workers: {workers}",
                    "Configuration:",
                    Syntax(config, "yaml", theme="monokai"),
                ),
                title="Setup Results",
            )
        )

    # Add command group to CLI
    cli.app.add_typer(config_group, name="config")

    # Build and run CLI
    cli_app = cli.build()
    cli_app()


if __name__ == "__main__":
    asyncio.run(main())
