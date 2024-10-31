from pepperpy.llm import get_llm

def demonstrate_llm_metrics():
    llm = get_llm("openrouter")
    
    # Estimativa prévia
    prompt = "Explique o conceito de programação funcional em Python"
    estimated_cost = llm.estimate_cost(prompt)
    print(f"Custo estimado: ${estimated_cost.total_cost:.4f}")
    print(f"Tokens estimados: {llm.estimate_tokens(prompt)}")
    
    # Executa a chamada
    response = llm.complete(prompt)
    print(f"\nResposta: {response.content}")
    print(f"\nUso real de tokens:")
    print(f"- Prompt: {response.usage.prompt_tokens}")
    print(f"- Completion: {response.usage.completion_tokens}")
    print(f"- Total: {response.usage.total_tokens}")
    
    if response.cost:
        print(f"\nCusto real:")
        print(f"- Prompt: ${response.cost.prompt_cost:.4f}")
        print(f"- Completion: ${response.cost.completion_cost:.4f}")
        print(f"- Total: ${response.cost.total_cost:.4f}")
    
    # Métricas acumuladas
    print(f"\nMétricas totais da sessão:")
    print(f"- Custo total: ${llm.total_cost:.4f}")
    print(f"- Tokens totais: {llm.total_tokens}")
    
    # Resetar métricas se necessário
    llm.reset_metrics()

if __name__ == "__main__":
    demonstrate_llm_metrics() 