from pepperpy.db import connect_db
from pepperpy.logging import get_logger

logger = get_logger()

def demonstrate_sqlite():
    conn = connect_db("example.db")
    cursor = conn.cursor()
    
    # Criar uma tabela de exemplo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            email TEXT
        )
    """)
    
    # Inserir alguns dados
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
    
    conn.close()

if __name__ == "__main__":
    demonstrate_sqlite() 