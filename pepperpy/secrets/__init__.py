"""Secure secrets management system."""
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass, field
import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from abc import ABC, abstractmethod
from ..core.config import Config
from ..logging import get_logger

logger = get_logger()

@dataclass
class SecretConfig:
    """Configuration for secrets management."""
    store_path: Union[str, Path] = "secrets"
    key_file: Union[str, Path] = ".key"
    salt_file: Union[str, Path] = ".salt"
    iterations: int = 100_000
    env_prefix: str = "PEPPERPY_"

class SecretStore(ABC):
    """Abstract base class for secret storage."""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a secret value."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a secret value."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a secret."""
        pass
    
    @abstractmethod
    def list_secrets(self) -> List[str]:
        """List all secret keys."""
        pass

class FileSecretStore(SecretStore):
    """File-based encrypted secret storage."""
    
    def __init__(self, config: SecretConfig):
        self.config = config
        self.store_path = Path(config.store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self._fernet = self._initialize_encryption()
    
    def _initialize_encryption(self) -> Fernet:
        """Initialize encryption with key derivation."""
        key_path = self.store_path / self.config.key_file
        salt_path = self.store_path / self.config.salt_file
        
        # Generate or load salt
        if salt_path.exists():
            with open(salt_path, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(salt_path, 'wb') as f:
                f.write(salt)
        
        # Generate or load key
        if key_path.exists():
            with open(key_path, 'rb') as f:
                key = base64.urlsafe_b64decode(f.read())
        else:
            # Generate key using PBKDF2
            master_key = os.urandom(32)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=self.config.iterations,
            )
            key = base64.urlsafe_b64encode(kdf.derive(master_key))
            with open(key_path, 'wb') as f:
                f.write(key)
        
        return Fernet(key)
    
    def _get_secret_path(self, key: str) -> Path:
        """Get path for a secret file."""
        return self.store_path / f"{key}.secret"
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a secret value."""
        # Check environment first
        env_key = f"{self.config.env_prefix}{key.upper()}"
        if env_value := os.getenv(env_key):
            return env_value
        
        # Then check file store
        secret_path = self._get_secret_path(key)
        if not secret_path.exists():
            return default
            
        try:
            with open(secret_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self._fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            logger.error(f"Error reading secret {key}: {str(e)}")
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a secret value."""
        try:
            # Serialize and encrypt
            data = json.dumps(value).encode()
            encrypted_data = self._fernet.encrypt(data)
            
            # Save to file
            secret_path = self._get_secret_path(key)
            with open(secret_path, 'wb') as f:
                f.write(encrypted_data)
                
            logger.debug(f"Secret {key} stored successfully")
            
        except Exception as e:
            logger.error(f"Error storing secret {key}: {str(e)}")
            raise
    
    def delete(self, key: str) -> None:
        """Delete a secret."""
        secret_path = self._get_secret_path(key)
        if secret_path.exists():
            secret_path.unlink()
            logger.debug(f"Secret {key} deleted")
    
    def list_secrets(self) -> List[str]:
        """List all secret keys."""
        return [
            p.stem for p in self.store_path.glob("*.secret")
        ]

class SecretsManager:
    """Central secrets management."""
    
    def __init__(
        self,
        config: Optional[SecretConfig] = None,
        store: Optional[SecretStore] = None
    ):
        self.config = config or SecretConfig()
        self.store = store or FileSecretStore(self.config)
    
    def get_secret(
        self,
        key: str,
        default: Any = None,
        required: bool = False
    ) -> Any:
        """Get a secret value."""
        value = self.store.get(key, default)
        if required and value is None:
            raise ValueError(f"Required secret {key} not found")
        return value
    
    def set_secret(self, key: str, value: Any) -> None:
        """Set a secret value."""
        self.store.set(key, value)
    
    def delete_secret(self, key: str) -> None:
        """Delete a secret."""
        self.store.delete(key)
    
    def list_secrets(self) -> List[str]:
        """List all secret keys."""
        return self.store.list_secrets()
    
    def rotate_keys(self) -> None:
        """Rotate encryption keys."""
        # Get all current secrets
        secrets = {
            key: self.get_secret(key)
            for key in self.list_secrets()
        }
        
        # Reinitialize encryption
        if isinstance(self.store, FileSecretStore):
            self.store._fernet = self.store._initialize_encryption()
        
        # Re-encrypt all secrets
        for key, value in secrets.items():
            self.set_secret(key, value)
            
        logger.info("Encryption keys rotated successfully")

# Global secrets manager
secrets = SecretsManager()

# Convenience functions
def get_secret(
    key: str,
    default: Any = None,
    required: bool = False
) -> Any:
    """Get a secret value."""
    return secrets.get_secret(key, default, required)

def set_secret(key: str, value: Any) -> None:
    """Set a secret value."""
    secrets.set_secret(key, value) 