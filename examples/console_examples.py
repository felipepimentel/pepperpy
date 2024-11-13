"""Console module examples demonstrating UI, CLI, and Rich console features"""

import asyncio
from typing import List

from rich.align import Align
from rich.box import DOUBLE, ROUNDED
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from pepperpy.console import Console
from pepperpy.console.ui import (
    ChatView,
    Dialog,
    Form,
    FormField,
    ListView,
    ProgressBar,
)
from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


async def demo_chat_view() -> None:
    """Demonstrate chat view component with rich formatting and emojis"""
    chat = ChatView()

    # Sistema iniciando com estilo
    chat.add_message("🚀 System v1.0 initialized", "system")
    chat.add_message(
        "Welcome to PepperPy Console Demo! How can I assist you today? 🤖", "assistant"
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
        chat.render(),
        title="[bold cyan]Chat Demo[/]",
        subtitle="[dim]Press Ctrl+C to continue[/]",
        border_style="cyan",
        box=ROUNDED,
        padding=(1, 2),
    )

    console = Console()
    console.print(panel)


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

        # Criar um painel para cada estágio
        panel = Panel(
            progress.render(),
            title=f"[bold {color}]{desc}[/]",
            border_style=color,
            box=ROUNDED,
        )

        for i in range(start, end + 1, 5):
            progress.set_progress(i, f"{desc} ({i}%)")
            console.clear()
            console.print(panel)
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
        )
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
        )
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
        )
    )

    def submit() -> None:
        console = Console()
        console.print("[bold green]✅ Form submitted successfully![/]")

    form.add_button("📤 Submit", submit)
    await form.initialize()

    # Criar layout com duas colunas
    layout = Layout()
    layout.split_column(
        Layout(
            Panel(
                form.render(),
                title="[bold blue]Registration Form[/]",
                border_style="blue",
                box=DOUBLE,
            ),
        ),
        Layout(
            Panel(
                "✨ Fill out the form above to register\n"
                "📝 All fields are required\n"
                "❓ Press Tab to navigate between fields\n"
                "↵  Press Enter to submit",
                title="[bold cyan]Instructions[/]",
                border_style="cyan",
                box=ROUNDED,
            ),
        ),
    )

    console = Console()
    console.print(layout)


async def demo_list_view() -> None:
    """Demonstrate advanced list view with categories and status indicators"""
    list_view = ListView[str]()

    # Items com ícones e status
    items: List[tuple] = [
        ("task1", "🟢 Deploy application", True),
        ("task2", "🟡 Review pull requests", True),
        ("task3", "🔴 Fix critical bug (Blocked)", False),
        ("task4", "⚪ Update documentation", True),
        ("task5", "🟣 Optimize database", True),
    ]

    for value, label, enabled in items:
        list_view.add_item(value, label, enabled)

    # Criar tabela de estatísticas
    stats_table = Table(box=ROUNDED, border_style="cyan")
    stats_table.add_column("Category", style="cyan")
    stats_table.add_column("Count", justify="right", style="green")

    stats = {
        "Active": sum(1 for _, _, e in items if e),
        "Blocked": sum(1 for _, _, e in items if not e),
        "Total": len(items),
    }

    for category, count in stats.items():
        stats_table.add_row(category, str(count))

    # Layout combinando lista e estatísticas
    layout = Layout()
    layout.split_row(
        Layout(
            Panel(
                list_view.render(),
                title="[bold blue]Task List[/]",
                border_style="blue",
                box=DOUBLE,
            ),
            ratio=2,
        ),
        Layout(
            Panel(
                Align.center(stats_table),
                title="[bold cyan]Statistics[/]",
                border_style="cyan",
                box=ROUNDED,
            ),
            ratio=1,
        ),
    )

    console = Console()
    console.print(layout)


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
    changes_table = Table(box=ROUNDED, show_header=False)
    changes_table.add_column("Change", style="cyan")
    for change in changes:
        changes_table.add_row(change)

    dialog.content = (
        f"[bold]Current version:[/] {current_version}\n"
        f"[bold]New version:[/] [green]{new_version}[/]\n\n"
        "[bold]Changes:[/]\n"
        f"{changes_table}"
    )

    def on_update() -> None:
        console = Console()
        console.print("[bold green]✅ Update started![/]")

    def on_cancel() -> None:
        console = Console()
        console.print("[bold yellow]⏸️ Update postponed[/]")

    dialog.add_button("🔄 Update Now", on_update)
    dialog.add_button("⏳ Remind Later", on_cancel)

    console = Console()
    console.print(dialog.render())


async def run_demos() -> None:
    """Run all demos with transitions"""
    console = Console()

    demos = [
        ("Chat View", demo_chat_view),
        ("Progress Bar", demo_progress_bar),
        ("Form", demo_form),
        ("List View", demo_list_view),
        ("Dialog", demo_dialog),
    ]

    for i, (name, demo) in enumerate(demos, 1):
        # Transição animada
        console.clear()
        console.print(
            Panel(
                f"[bold cyan]Demo {i}/{len(demos)}:[/] [bold blue]{name}[/]",
                border_style="cyan",
                box=ROUNDED,
            )
        )
        await asyncio.sleep(1)

        # Executar demo
        await demo()

        if i < len(demos):
            # Aguardar input do usuário
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    console = Console()
    try:
        asyncio.run(run_demos())
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Demo finished![/] 👋")
