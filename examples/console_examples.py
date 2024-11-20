"""Console module examples demonstrating UI, CLI, and Rich console features"""

import asyncio
from typing import Any

from rich.text import Text

from pepperpy.console import Console
from pepperpy.console.ui import (
    ChatView,
    Dialog,
    Form,
    FormField,
    Layout,
    ListView,
    Panel,
    PanelConfig,
    ProgressBar,
    Table,
    TableConfig,
)


async def render_and_print(console: Console, content: Any) -> None:
    """Render and print content"""
    if hasattr(content, "render"):
        rendered = await content.render()
        console.print(rendered)
    else:
        console.print(content)


async def demo_chat_view() -> None:
    """Demonstrate chat view component with rich formatting and emojis"""
    chat = ChatView()

    # Sistema iniciando com estilo
    chat.add_message("🚀 System v1.0 initialized", "system")
    chat.add_message(
        "Welcome to PepperPy Console Demo! How can I assist you today? 🤖",
        "assistant",
    )
    chat.add_message("I'd like to see what this console can do! 👀", "user")
    chat.add_message(
        "Let me show you some amazing features! Here's what we have:\n"
        "✨ Rich text formatting\n"
        "📊 Progress tracking\n"
        "📝 Interactive forms\n"
        "📋 Dynamic lists\n"
        "🔍 Smart dialogs\n"
        "Let's explore them together! 🎉",
        "assistant",
    )

    # Criar um painel estilizado para o chat
    panel = Panel(
        content=chat,
        config=PanelConfig(
            title="Chat Demo",
            subtitle="Press Ctrl+C to continue",
            style="cyan",
            border_style="rounded",
        ),
    )

    console = Console()
    await render_and_print(console, panel)


async def demo_progress_bar() -> None:
    """Demonstrate advanced progress bar with multiple stages"""
    console = Console()
    progress = ProgressBar(total=100)

    stages = [
        ("🔍 Analyzing data", "cyan"),
        ("📦 Processing files", "green"),
        ("🔄 Optimizing results", "yellow"),
        ("✨ Finalizing", "magenta"),
    ]

    for stage_num, (desc, color) in enumerate(stages):
        start = stage_num * 25
        end = (stage_num + 1) * 25

        panel = Panel(
            content=progress, config=PanelConfig(title=desc, style=color, border_style="rounded")
        )

        for i in range(start, end + 1, 5):
            progress.set_progress(i, f"{desc} ({i}%)")
            console.clear()
            await render_and_print(console, panel)
            await asyncio.sleep(0.2)


async def demo_form() -> None:
    """Demonstrate interactive form with validation and rich formatting"""
    form = Form()

    # Campos do formulário com validação avançada
    form.add_field(
        FormField(
            name="username",
            label="👤 Username",
            required=True,
            validators=[
                lambda x: len(x) >= 3,
                lambda x: x.isalnum(),
            ],
        ),
    )

    form.add_field(
        FormField(
            name="email",
            label="📧 Email",
            required=True,
            validators=[
                lambda x: "@" in x,
                lambda x: "." in x.split("@")[1],
            ],
        ),
    )

    form.add_field(
        FormField(
            name="role",
            label="🎭 Role",
            required=True,
            validators=[
                lambda x: x in ["Developer", "Designer", "Manager"],
            ],
            metadata={
                "hint": "Enter one of: Developer, Designer, Manager",
            },
        ),
    )

    def submit() -> None:
        console = Console()
        console.success("Form submitted successfully!")

    form.add_button("📤 Submit", submit)
    await form.initialize()

    # Criar layout com duas colunas
    layout = Layout()
    await layout.split(
        Panel(
            content=form,
            config=PanelConfig(title="Registration Form", style="blue", border_style="double"),
        ),
        Panel(
            content=(
                "✨ Fill out the form above to register\n"
                "📝 All fields are required\n"
                "❓ Press Tab to navigate between fields\n"
                "↵  Press Enter to submit"
            ),
            config=PanelConfig(title="Instructions", style="cyan", border_style="rounded"),
        ),
        direction="vertical",
    )

    console = Console()
    await render_and_print(console, layout)


async def demo_list_view() -> None:
    """Demonstrate advanced list view with categories and status indicators"""
    list_view = ListView[str]()

    # Items com ícones e status
    items: list[tuple] = [
        ("task1", "🟢 Deploy application", True),
        ("task2", "🟡 Review pull requests", True),
        ("task3", "🔴 Fix critical bug (Blocked)", False),
        ("task4", "⚪ Update documentation", True),
        ("task5", "🟣 Optimize database", True),
    ]

    for value, label, enabled in items:
        list_view.add_item(value, label, enabled)

    # Criar tabela de estatísticas com configuração adequada
    stats_table = Table(
        TableConfig(title="Task Statistics", style="cyan", show_header=True, padding=(0, 1))
    )

    stats_table.add_column("Category", style="cyan")
    stats_table.add_column("Count", align="right", style="green")

    stats = {
        "Active": sum(1 for _, _, e in items if e),
        "Blocked": sum(1 for _, _, e in items if not e),
        "Total": len(items),
    }

    for category, count in stats.items():
        stats_table.add_row(category, str(count))

    # Layout combinando lista e estatísticas
    layout = Layout()
    await layout.split(
        Panel(
            content=list_view,
            config=PanelConfig(title="Task List", style="blue", border_style="double"),
        ),
        Panel(
            content=stats_table,
            config=PanelConfig(title="Statistics", style="cyan", border_style="rounded"),
        ),
        direction="horizontal",
        ratios=[2, 1],
    )

    console = Console()
    await render_and_print(console, layout)


async def demo_dialog() -> None:
    """Demonstrate rich dialog with dynamic content"""
    dialog = Dialog()
    dialog.title = "🔔 Important Update Available"

    # Conteúdo dinâmico com estatísticas
    current_version = "1.2.3"
    new_version = "2.0.0"
    changes = [
        "✨ New user interface",
        "🚀 Improved performance",
        "🐛 Bug fixes",
        "📦 Updated dependencies",
    ]

    # Criar tabela de mudanças
    changes_table = Table(TableConfig(style="cyan", show_header=False, padding=(0, 1)))
    changes_table.add_column("Change", style="cyan")

    for change in changes:
        changes_table.add_row(change)

    # Criar o conteúdo completo
    content_text = (
        f"Current version: {current_version}\n" f"New version: {new_version}\n\n" "Changes:\n"
    )

    # Criar um Text para combinar texto e tabela
    content = Text(content_text)
    rendered_table = await changes_table.render()
    content.append(str(rendered_table))

    dialog.content = content

    def on_update() -> None:
        console = Console()
        console.success("Update started!")

    def on_cancel() -> None:
        console = Console()
        console.warning("Update postponed")

    dialog.add_button("🔄 Update Now", on_update, style="green")
    dialog.add_button("⏳ Remind Later", on_cancel, style="yellow")

    console = Console()
    await render_and_print(console, dialog)


if __name__ == "__main__":
    try:
        asyncio.run(demo_chat_view())
        asyncio.run(demo_progress_bar())
        asyncio.run(demo_form())
        asyncio.run(demo_list_view())
        asyncio.run(demo_dialog())
    except KeyboardInterrupt:
        console = Console()
        console.info("Examples finished! 👋")
