import asyncio

import typer

from pepperpy.console import ConsoleModule
from pepperpy.core import Application
from pepperpy.core.builder import CLIBuilder


async def main() -> None:
    # Create application
    app = Application()

    # Configure console module
    console = (
        ConsoleModule.create()
        .configure(theme={"info": "cyan", "success": "green bold", "error": "red bold"})
        .build()
    )

    app.add_module(console)

    # Create CLI
    cli = CLIBuilder(name="mycli", help="Example CLI application", version="1.0.0")

    @cli.command(help="Greet a user")
    async def greet(
        name: str = typer.Argument(..., help="User name"),
        count: int = typer.Option(1, help="Number of greetings"),
    ) -> None:
        """Greet user multiple times"""
        for i in range(count):
            console.success(f"Hello {name}! (greeting {i+1}/{count})")

    @cli.command(help="Process items")
    async def process() -> None:
        """Process items with progress"""
        items = ["item1", "item2", "item3"]

        with console.status("Processing items..."):
            for item in items:
                await asyncio.sleep(1)  # Simulate work
                console.info(f"Processed {item}")

        # Create table
        table = console.create_table(
            title="Processing Results", headers=["Item", "Status"]
        )
        for item in items:
            table.add_row(item, "✅")

        console.print(table)

    # Build and run CLI
    cli_app = cli.build()
    cli_app()


if __name__ == "__main__":
    asyncio.run(main())
