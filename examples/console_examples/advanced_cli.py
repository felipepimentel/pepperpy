import asyncio

from pepperpy.console import ConsoleModule
from pepperpy.core import Application
from pepperpy.core.builder import CLIBuilder


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

    # Create CLI
    cli = CLIBuilder(name="mycli", help="Example CLI application", version="1.0.0")

    @cli.command(
        name="greet",
        help="Greet a user",
        arguments=[{"name": "name", "help": "User name"}],
        options=[
            {
                "name": "--count",
                "help": "Number of greetings",
                "type": int,
                "default": 1,
            }
        ],
    )
    async def greet(name: str, count: int) -> None:
        """Greet user multiple times"""
        for _ in range(count):
            console.success(f"Hello {name}!")

    @cli.command(name="process", help="Process items with progress")
    async def process() -> None:
        """Process items with progress bar"""
        items = ["item1", "item2", "item3"]

        with console.status("Processing items..."):
            for item in items:
                await asyncio.sleep(1)  # Simulate work
                console.info(f"Processed {item}")

    # Build and run CLI
    cli_app = cli.build()
    cli_app()


if __name__ == "__main__":
    asyncio.run(main())
