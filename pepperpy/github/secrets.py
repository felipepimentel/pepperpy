"""GitHub Secrets management."""
from typing import Dict, List, Optional
from nacl import encoding, public

from .core import GitHubManager

class SecretsManager:
    """Manage GitHub Secrets."""
    
    def __init__(self, github: GitHubManager):
        self.github = github
        
    def _encrypt(self, public_key: str, secret_value: str) -> str:
        """Encrypt a secret using repository public key."""
        public_key_bytes = public.PublicKey(
            public_key.encode("utf-8"),
            encoding.Base64Encoder()
        )
        sealed_box = public.SealedBox(public_key_bytes)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return encoding.Base64Encoder().encode(encrypted).decode("utf-8")
        
    async def set_secret(
        self,
        repo: str,
        name: str,
        value: str,
        visibility: str = "selected"
    ) -> None:
        """Set a repository secret."""
        repository = await self.github.get_repository(repo)
        
        # Get repository public key
        public_key = repository.get_public_key()
        
        # Encrypt secret
        encrypted_value = self._encrypt(public_key.key, value)
        
        # Create/update secret
        repository.create_secret(
            name,
            encrypted_value,
            public_key.key_id,
            visibility
        )
        
    async def delete_secret(self, repo: str, name: str) -> None:
        """Delete a repository secret."""
        repository = await self.github.get_repository(repo)
        repository.delete_secret(name)
        
    async def list_secrets(self, repo: str) -> List[str]:
        """List repository secrets."""
        repository = await self.github.get_repository(repo)
        return [secret.name for secret in repository.get_secrets()] 