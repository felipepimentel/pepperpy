"""Example of secrets management."""
from pepperpy.secrets import (
    SecretsManager,
    SecretConfig,
    get_secret,
    set_secret
)

def demonstrate_secrets():
    """Demonstrate secrets management functionality."""
    # Configure secrets manager
    config = SecretConfig(
        store_path="./secure",
        env_prefix="MYAPP_"
    )
    secrets = SecretsManager(config)
    
    # Store some secrets
    secrets.set_secret(
        "database",
        {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "super_secret"
        }
    )
    
    secrets.set_secret(
        "api_key",
        "sk_test_123456789"
    )
    
    # Retrieve secrets
    db_config = secrets.get_secret("database")
    print("Database Configuration:")
    print(f"Host: {db_config['host']}")
    print(f"Port: {db_config['port']}")
    print(f"Username: {db_config['username']}")
    print(f"Password: {'*' * len(db_config['password'])}")
    
    api_key = secrets.get_secret("api_key")
    print(f"\nAPI Key: {api_key[:5]}...")
    
    # List all secrets
    print("\nAll secrets:")
    for key in secrets.list_secrets():
        print(f"- {key}")
    
    # Using convenience functions
    set_secret("app_secret", "my_app_secret")
    app_secret = get_secret("app_secret")
    print(f"\nApp Secret: {app_secret}")
    
    # Rotate encryption keys
    print("\nRotating encryption keys...")
    secrets.rotate_keys()
    
    # Verify secrets after rotation
    rotated_secret = secrets.get_secret("app_secret")
    print(f"Secret after rotation: {rotated_secret}")
    
    # Cleanup
    secrets.delete_secret("app_secret")
    print("\nRemaining secrets:")
    for key in secrets.list_secrets():
        print(f"- {key}")

if __name__ == "__main__":
    demonstrate_secrets() 