from datetime import datetime
from pathlib import Path

from pepperpy.console import Console, ConsoleTemplates, Style
from pepperpy.console.interactive.widgets import InteractiveWidgets
from pepperpy.console.visualization.charts import ChartTheme, ConsoleCharts


async def demo_basic_output(console: Console) -> None:
    """Demonstrate basic console output capabilities"""
    console.title("Basic Console Output Demo")

    # Basic logging with different styles
    console.info("Starting console demonstration...")
    console.success("Configuration loaded successfully")
    console.warning("Cache size is approaching limit")
    console.error("Failed to connect to remote service")

    # Custom styling
    console.print("Custom styled text", style=Style.HIGHLIGHT)
    console.print("Code example: console.print()", style=Style.CODE)
    console.print("https://github.com/example/pepperpy", style=Style.URL)

    console.divider()


async def demo_data_display(console: Console) -> None:
    """Demonstrate data visualization capabilities"""
    console.title("Data Display Demo")

    # Sample data
    user_data = [
        {"id": 1, "name": "Alice", "role": "Admin", "active": True},
        {"id": 2, "name": "Bob", "role": "User", "active": True},
        {"id": 3, "name": "Charlie", "role": "User", "active": False},
    ]

    # Display as table
    console.info("User Data Table:")
    console.table(user_data, title="System Users")

    # Display as JSON
    console.info("\nUser Data JSON:")
    console.show(user_data, title="Users JSON View")

    console.divider()


async def demo_interactive_input(console: Console) -> None:
    """Demonstrate interactive input features"""
    console.title("Interactive Input Demo")

    # Basic input
    name = console.ask("What's your name?")
    console.info(f"Hello, {name}!")

    # Choice selection
    role = console.ask(
        "Select your role:", choices=["Admin", "User", "Guest"], default="User"
    )
    console.success(f"Role selected: {role}")

    # Confirmation
    if console.confirm("Would you like to continue?"):
        console.info("Continuing...")
    else:
        console.warning("Operation cancelled")

    console.divider()


async def demo_progress_tracking(console: Console) -> None:
    """Demonstrate progress tracking"""
    console.title("Progress Tracking Demo")

    # Simple progress tracking
    with console.progress("Processing files...") as progress:
        for _ in range(5):
            await asyncio.sleep(0.5)  # Simulate work
            progress.update(0, advance=0.2)

    console.success("Processing complete!")
    console.divider()


async def demo_advanced_widgets(console: Console) -> None:
    """Demonstrate advanced interactive widgets"""
    console.title("Advanced Widgets Demo")

    widgets = InteractiveWidgets(console.console)

    # Date picker
    selected_date = await widgets.date_picker("Select start date:")
    console.info(f"Selected date: {selected_date}")

    # Tag input
    tags = await widgets.tag_input(
        message="Enter project tags",
        suggestions=["python", "web", "api", "database", "async"],
    )
    console.info(f"Selected tags: {', '.join(tags)}")

    console.divider()


async def demo_visualization(console: Console) -> None:
    """Demonstrate data visualization capabilities"""
    console.title("Data Visualization Demo")

    charts = ConsoleCharts(
        console.console,
        theme=ChartTheme(background="#1a1a1a", foreground="#ffffff", accent="#00ff00"),
    )

    # Sample data for charts
    data = {
        "Revenue": [100, 120, 115, 130, 140, 138, 145],
        "Users": [50, 55, 65, 75, 80, 85, 90],
    }

    # Line chart
    charts.line_chart(data, title="Weekly Metrics", width=60, height=20)

    # Histogram
    charts.histogram([1, 2, 2, 3, 3, 3, 4, 4, 5], bins=5, title="Data Distribution")

    console.divider()


async def main() -> None:
    """Main demo function"""
    # Initialize console with custom templates
    console = Console()
    ConsoleTemplates.add("demo_start", "Starting $demo_name demonstration...")
    ConsoleTemplates.add("demo_end", "Completed $demo_name demonstration")

    # Clear screen and show welcome message
    console.clear()
    console.print("PepperPy Console Demonstration", style=Style.HIGHLIGHT)
    console.print("================================\n")

    # Run demonstrations
    demos = [
        ("Basic Output", demo_basic_output),
        ("Data Display", demo_data_display),
        ("Interactive Input", demo_interactive_input),
        ("Progress Tracking", demo_progress_tracking),
        ("Advanced Widgets", demo_advanced_widgets),
        ("Data Visualization", demo_visualization),
    ]

    for demo_name, demo_func in demos:
        console.log(ConsoleTemplates.get("demo_start", demo_name=demo_name))
        await demo_func(console)
        console.log(ConsoleTemplates.get("demo_end", demo_name=demo_name))
        await asyncio.sleep(1)

    # Save demo results
    results = {
        "timestamp": datetime.now().isoformat(),
        "demos_completed": len(demos),
        "status": "success",
    }

    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    console.save_json(results, output_dir / "demo_results.json")
    console.success("Demo completed! Results saved to demo_output/demo_results.json")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
