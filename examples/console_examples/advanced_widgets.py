import asyncio
import random
from datetime import date, timedelta

from pepperpy.console import ConsoleModule
from pepperpy.console.interactive.widgets import InteractiveWidgets
from pepperpy.core import Application


async def main():
    # Configure console
    app = Application()
    console = (
        ConsoleModule.create()
        .configure(theme={"info": "cyan", "success": "green bold", "error": "red bold"})
        .build()
    )

    app.add_module(console)

    async with app.run():
        # Create widgets
        widgets = InteractiveWidgets(console._console)

        # Search select example
        countries = [
            "Brazil",
            "Canada",
            "China",
            "France",
            "Germany",
            "India",
            "Japan",
            "UK",
            "USA",
        ]
        country = await widgets.search_select(countries, message="Select country:")
        console.info(f"Selected country: {country}")

        # Date picker example
        start_date = await widgets.date_picker(
            "Select start date:",
            min_date=date.today() - timedelta(days=365),
            max_date=date.today(),
        )
        console.info(f"Selected date: {start_date}")

        # Color picker example
        color = await widgets.color_picker("Select theme color:")
        console.info(f"Selected color: {color}")

        # Tag input example
        technologies = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "Docker",
            "Kubernetes",
            "AWS",
            "Azure",
        ]
        tags = await widgets.tag_input(
            "Enter technologies:", suggestions=technologies, max_tags=5
        )
        console.info(f"Selected tags: {', '.join(tags)}")

        # Charts example
        charts = console.charts

        # Line chart
        data = {
            "Series A": [random.randint(0, 100) for _ in range(10)],
            "Series B": [random.randint(0, 100) for _ in range(10)],
        }
        charts.line_chart(data, "Multi-line Chart")

        # Scatter plot
        x = [random.uniform(0, 10) for _ in range(20)]
        y = [random.uniform(0, 10) for _ in range(20)]
        charts.scatter_plot(x, y, title="Scatter Plot")

        # Heatmap
        matrix = [[random.random() for _ in range(5)] for _ in range(5)]
        charts.heatmap(
            matrix,
            x_labels=["A", "B", "C", "D", "E"],
            y_labels=["1", "2", "3", "4", "5"],
            title="Heatmap",
        )

        # Box plot
        data = [[random.gauss(0, 1) for _ in range(100)] for _ in range(3)]
        charts.box_plot(
            data, labels=["Group A", "Group B", "Group C"], title="Box Plot"
        )


if __name__ == "__main__":
    asyncio.run(main())
