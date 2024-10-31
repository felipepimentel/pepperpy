from pepperpy.api_request import fetch_data, post_data
from pepperpy.logging import get_logger

logger = get_logger()

def demonstrate_api():
    # Exemplo usando uma API pública
    try:
        # GET request
        logger.info("🌐 Buscando dados da API...")
        data = fetch_data("https://jsonplaceholder.typicode.com/posts/1")
        logger.info(f"📥 Dados recebidos: {data}")
        
        # POST request
        new_post = {
            "title": "Exemplo Pepperpy",
            "body": "Este é um exemplo de POST request",
            "userId": 1
        }
        
        logger.info("📤 Enviando dados para API...")
        response = post_data("https://jsonplaceholder.typicode.com/posts", new_post)
        logger.info(f"✅ Resposta do servidor: {response}")
        
    except Exception as e:
        logger.error(f"❌ Erro na requisição: {str(e)}")

if __name__ == "__main__":
    demonstrate_api() 