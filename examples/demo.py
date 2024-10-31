from pepperpy.logging import get_logger
from pepperpy.console import print_message, print_table
from pepperpy.file import read_json, write_json, read_csv, write_csv
from pepperpy.db import connect_db
from pepperpy.api_request import fetch_data, post_data

logger = get_logger()

def separator(title):
    print_message(f"\n[bold blue]{'='*20} {title} {'='*20}[/]\n")

def demo_logging():
    separator("Demo: Logging")
    logger.debug("🔍 Debug: Detalhando variáveis do sistema")
    logger.info("ℹ️ Info: Aplicação iniciada com sucesso")
    logger.warning("⚠️ Warning: Espaço em disco está ficando baixo")
    logger.error("❌ Error: Falha ao conectar com o banco de dados")
    logger.critical("🚨 Critical: Sistema em estado crítico!")

def demo_console():
    separator("Demo: Console")
    print_message("[bold green]Bem-vindo ao Pepperpy![/]")
    
    data = [
        {"Nome": "João", "Idade": 30, "Cidade": "São Paulo"},
        {"Nome": "Maria", "Idade": 25, "Cidade": "Rio de Janeiro"},
        {"Nome": "Pedro", "Idade": 35, "Cidade": "Belo Horizonte"}
    ]
    print_table(data)

def demo_files():
    separator("Demo: Operações com Arquivos")
    
    # JSON demo
    config_data = {
        "nome": "Pepperpy",
        "versão": "1.0.0",
        "configurações": {
            "debug": True,
            "log_level": "INFO"
        }
    }
    
    logger.info("📝 Salvando arquivo JSON...")
    write_json(config_data, "demo_config.json")
    loaded_json = read_json("demo_config.json")
    logger.info(f"📄 JSON carregado: {loaded_json}")
    
    # CSV demo
    csv_data = [
        ["Nome", "Idade", "Cidade"],
        ["João", "30", "São Paulo"],
        ["Maria", "25", "Rio de Janeiro"]
    ]
    
    logger.info("📝 Salvando arquivo CSV...")
    write_csv(csv_data, "demo_dados.csv")
    loaded_csv = read_csv("demo_dados.csv")
    logger.info(f"📊 CSV carregado: {loaded_csv}")

def demo_database():
    separator("Demo: Banco de Dados")
    conn = connect_db("demo.db")
    cursor = conn.cursor()
    
    try:
        # Criar e popular tabela
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                email TEXT
            )
        """)
        
        usuarios = [
            ("João Silva", "joao@email.com"),
            ("Maria Santos", "maria@email.com")
        ]
        
        cursor.executemany("INSERT INTO usuarios (nome, email) VALUES (?, ?)", usuarios)
        conn.commit()
        
        # Consultar dados
        cursor.execute("SELECT * FROM usuarios")
        results = cursor.fetchall()
        
        logger.info("📚 Usuários cadastrados:")
        for row in results:
            logger.info(f"ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}")
            
    finally:
        conn.close()

def demo_api():
    separator("Demo: Requisições API")
    try:
        # GET request
        logger.info("🌐 GET: Buscando post...")
        post = fetch_data("https://jsonplaceholder.typicode.com/posts/1")
        logger.info(f"📥 Dados recebidos: {post}")
        
        # POST request
        new_post = {
            "title": "Demo Pepperpy",
            "body": "Este é um exemplo de POST request",
            "userId": 1
        }
        
        logger.info("📤 POST: Enviando dados...")
        response = post_data("https://jsonplaceholder.typicode.com/posts", new_post)
        logger.info(f"✅ Resposta: {response}")
        
    except Exception as e:
        logger.error(f"❌ Erro na requisição: {str(e)}")

def run_demo():
    print_message("[bold green]🚀 Iniciando Demo Completa do Pepperpy[/]")
    
    # Executar todas as demos
    demo_logging()
    demo_console()
    demo_files()
    demo_database()
    demo_api()
    
    print_message("\n[bold green]✨ Demo Completa Finalizada![/]")

if __name__ == "__main__":
    run_demo() 