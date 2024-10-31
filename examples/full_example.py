from pepperpy.logging import get_logger
from pepperpy.console import print_message, print_table
from pepperpy.file import write_json, read_json
from pepperpy.db import connect_db
from pepperpy.api_request import fetch_data

logger = get_logger()

def run_full_demo():
    logger.info("🚀 Iniciando demonstração completa do Pepperpy")
    
    # Console demo
    print_message("[bold blue]===== Demo Pepperpy =====[/]")
    
    # API demo
    logger.info("📡 Buscando dados da API...")
    try:
        post = fetch_data("https://jsonplaceholder.typicode.com/posts/1")
        
        # Salvando resultado em JSON
        write_json(post, "api_result.json")
        logger.info("💾 Dados da API salvos em arquivo JSON")
        
        # Mostrando em tabela
        print_table([post])
        
    except Exception as e:
        logger.error(f"Erro ao buscar dados: {e}")
    
    # Database demo
    logger.info("🗄️ Testando conexão com banco de dados...")
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS demo (
                id INTEGER PRIMARY KEY,
                info TEXT
            )
        """)
        logger.info("✅ Banco de dados configurado com sucesso")
    finally:
        conn.close()
    
    logger.info("🎉 Demonstração completa finalizada!")

if __name__ == "__main__":
    run_full_demo() 