"""Example of database usage."""
import asyncio
from pepperpy.database import database_connection, DatabaseConfig

async def demonstrate_database():
    """Demonstrate database functionality."""
    # Connect to database
    async with database_connection(
        "postgresql://user:pass@localhost/dbname",
        pool_size=5,
        ssl=True
    ) as db:
        # Create table
        await db.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        
        # Insert data using transaction
        async with db.transaction() as transaction:
            await transaction.execute("""
                INSERT INTO users (name, email) VALUES ($1, $2)
                """, 
                ("John Doe", "john@example.com")
            )
        
        # Fetch data
        users = await db.fetch_all(
            "SELECT * FROM users WHERE name LIKE $1",
            ("%John%",)
        )
        
        print("Users found:")
        for user in users:
            print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")

def main():
    """Run the demonstration."""
    asyncio.run(demonstrate_database())

if __name__ == "__main__":
    main() 