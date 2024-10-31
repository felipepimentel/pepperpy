from pepperpy.llm import get_llm

def demonstrate_llm():
    # Uso com Stackspot AI e conversação contínua
    stackspot = get_llm("stackspot")
    
    # Primeira mensagem da conversa
    response1 = stackspot.chat(
        messages=[
            {"role": "system", "content": "Você é um assistente Python especialista."},
            {"role": "user", "content": "Como criar um decorator?"}
        ],
        workspace_id="meu-workspace"
    )
    
    # Pega o conversation_id da resposta
    conversation_id = response1["metadata"]["conversation_id"]
    print(f"Primeira resposta: {response1['content']}")
    
    # Continua a mesma conversa
    response2 = stackspot.chat(
        messages=[
            {"role": "user", "content": "Pode dar um exemplo prático?"}
        ],
        conversation_id=conversation_id,
        workspace_id="meu-workspace"
    )
    print(f"Segunda resposta: {response2['content']}")
    
    # Exemplo com OpenRouter
    openrouter = get_llm("openrouter")
    response = openrouter.complete(
        "Explique programação funcional",
        model="anthropic/claude-3-sonnet",
        temperature=0.7,
        top_p=0.9,
        presence_penalty=0.1
    )
    print(f"OpenRouter resposta: {response['content']}")

if __name__ == "__main__":
    demonstrate_llm() 