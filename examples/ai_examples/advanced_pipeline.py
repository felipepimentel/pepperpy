from pepperpy.ai import AIModule
from pepperpy.core import Application


async def main():
    # Configure AI module
    app = Application()

    # Configure console module
    ai = (
        AIModule.create()
        .configure(
            # Configuração aqui
        )
        .build()
    )

    app.add_module(ai)
