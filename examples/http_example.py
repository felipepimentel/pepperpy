"""Example of HTTP client usage."""
import asyncio
from pepperpy.http import (
    create_client,
    create_api_client,
    HTTPConfig
)
from pepperpy.cache.base import MemoryCache

async def demonstrate_http():
    """Demonstrate HTTP client functionality."""
    # Basic HTTP client
    config = HTTPConfig(
        timeout=10.0,
        max_retries=3,
        cache_enabled=True
    )
    
    client = create_client(
        config=config,
        cache=MemoryCache()
    )
    
    try:
        # GET request
        response = await client.get(
            "https://jsonplaceholder.typicode.com/posts/1"
        )
        print("GET Response:", response)
        
        # POST request
        new_post = {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
        response = await client.post(
            "https://jsonplaceholder.typicode.com/posts",
            json=new_post
        )
        print("\nPOST Response:", response)
        
    finally:
        await client.close()
    
    # API client with authentication
    api = create_api_client(
        base_url="https://api.example.com",
        auth_token="your-token-here",
        config=HTTPConfig(
            timeout=5.0,
            verify_ssl=True
        )
    )
    
    try:
        # API endpoints
        users = await api.get("/users")
        print("\nUsers:", users)
        
        new_user = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        user = await api.post("/users", json=new_user)
        print("\nCreated User:", user)
        
    finally:
        await api.close()

def main():
    """Run the demonstration."""
    asyncio.run(demonstrate_http())

if __name__ == "__main__":
    main() 