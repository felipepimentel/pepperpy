"""Example of AI module usage."""
import asyncio
from pepperpy.ai import setup
from pepperpy.ai.core.config import AIConfig

async def demonstrate_ai():
    """Demonstrate AI capabilities."""
    # Configuração via código
    ai = setup({
        "llm_provider": "stackspot",
        "default_model": "gpt-4",
        "max_cost": 10.0
    })

    # Ou via arquivo de configuração
    # ai = setup.from_config("ai_config.yml")

    # Uso do RAG
    docs = ai.rag.load_documents("docs/")
    response = await ai.rag.query(
        "Como funciona o sistema?",
        documents=docs
    )
    print(f"RAG Response: {response['answer']}")

    # Uso de agentes
    result = await ai.agents.execute_task(
        "analyze_code",
        code="def hello(): print('world')"
    )
    print(f"Agent Result: {result}")

def main():
    """Run the demonstration."""
    asyncio.run(demonstrate_ai())

if __name__ == "__main__":
    main() 