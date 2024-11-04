import asyncio
import json

from pepperpy.ai import AIModule
from pepperpy.core import Application

# Example templates file (templates.yaml):
"""
templates:
  summarize:
    description: "Summarize text with specific focus"
    template: |
      Please summarize the following text, focusing on {{ focus }}:

      {{ text }}

      Key points to address:
      {% for point in points %}
      - {{ point }}
      {% endfor %}

  analyze:
    description: "Analyze text for specific aspects"
    template: |
      Analyze the following text for {{ aspect }}:

      {{ text }}

      Consider these factors:
      {% for factor in factors %}
      - {{ factor }}
      {% endfor %}
"""


async def main():
    # Configure AI module
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-key",
                "default_model": "anthropic/claude-3-opus",
            },
            templates_file="templates.yaml",
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        ai_module = app.get_module("ai", AIModule)

        # Use template for summarization
        summary = await ai_module.generate_from_template(
            "summarize",
            variables={
                "text": "Long text to summarize...",
                "focus": "technical aspects",
                "points": [
                    "Implementation details",
                    "Performance considerations",
                    "Security implications",
                ],
            },
        )
        print("Summary:", summary.content)

        # Use template for analysis
        analysis = await ai_module.generate_from_template(
            "analyze",
            variables={
                "text": "Text to analyze...",
                "aspect": "code quality",
                "factors": ["Maintainability", "Testability", "Performance"],
            },
        )
        print("\nAnalysis:", analysis.content)

        # Get metrics
        metrics = ai_module.get_metrics()
        print("\nMetrics:", json.dumps(metrics, indent=2))

        # Export metrics
        ai_module.export_metrics("ai_metrics.json")


if __name__ == "__main__":
    asyncio.run(main())
