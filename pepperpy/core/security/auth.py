"""Authentication and authorization implementation"""

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import AuthError


@dataclass
class AuthToken:
    """Authentication token data"""

    token: str
    expires_at: datetime
    user_id: str
    metadata: Dict[str, str]


class AuthManager(BaseModule):
    """Manager for authentication and authorization"""

    def __init__(self):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="auth",
            version="1.0.0",
            description="Authentication and authorization",
            dependencies=[],
            config={},
        )
        self._secret = None
        self._tokens = {}

    async def _setup(self) -> None:
        """Initialize auth manager"""
        self._secret = secrets.token_hex(32)

    async def _cleanup(self) -> None:
        """Cleanup auth resources"""
        self._tokens.clear()
        self._secret = None

    def _generate_salt(self) -> str:
        """Generate random salt"""
        return secrets.token_hex(16)

    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt"""
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100000, dklen=32
        ).hex()

    async def register(self, user_id: str, password: str) -> None:
        """Register new user"""
        try:
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)

            # Store user credentials (in a real system, this would go to a database)
            self._tokens[user_id] = {"salt": salt, "password_hash": password_hash}

        except Exception as e:
            raise AuthError(f"Registration failed: {str(e)}", cause=e)

    async def authenticate(self, user_id: str, password: str) -> AuthToken:
        """Authenticate user and generate token"""
        try:
            if user_id not in self._tokens:
                raise AuthError("User not found")

            stored = self._tokens[user_id]
            password_hash = self._hash_password(password, stored["salt"])

            if not hmac.compare_digest(password_hash, stored["password_hash"]):
                raise AuthError("Invalid password")

            # Generate JWT token
            expires_at = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode(
                {"user_id": user_id, "exp": expires_at}, self._secret, algorithm="HS256"
            )

            return AuthToken(token=token, expires_at=expires_at, user_id=user_id, metadata={})

        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Authentication failed: {str(e)}", cause=e)

    async def verify_token(self, token: str) -> Optional[str]:
        """Verify authentication token"""
        try:
            payload = jwt.decode(token, self._secret, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired")
        except jwt.InvalidTokenError as e:
            raise AuthError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise AuthError(f"Token verification failed: {str(e)}", cause=e)


# Global auth manager instance
auth = AuthManager()
