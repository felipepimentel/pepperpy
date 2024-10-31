"""Authentication and authorization system."""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import jwt
from abc import ABC, abstractmethod
from ..core.config import Config
from ..core.errors import AuthError

@dataclass
class AuthConfig:
    """Authentication configuration."""
    secret_key: str
    token_expiration: int = 3600  # 1 hour
    refresh_token_expiration: int = 604800  # 1 week
    algorithm: str = "HS256"
    token_type: str = "Bearer"

@dataclass
class UserCredentials:
    """User credentials for authentication."""
    username: str
    password: str

@dataclass
class TokenPair:
    """Access and refresh token pair."""
    access_token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = "Bearer"

@dataclass
class Permission:
    """Represents a system permission."""
    name: str
    description: str
    resource: str
    action: str

@dataclass
class Role:
    """Represents a user role with permissions."""
    name: str
    description: str
    permissions: List[Permission] = field(default_factory=list)

class AuthProvider(ABC):
    """Base class for authentication providers."""
    
    @abstractmethod
    async def authenticate(
        self,
        credentials: UserCredentials
    ) -> Dict[str, Any]:
        """Authenticate user credentials."""
        pass
    
    @abstractmethod
    async def validate_token(
        self,
        token: str
    ) -> Dict[str, Any]:
        """Validate authentication token."""
        pass

class AuthManager:
    """Central authentication and authorization manager."""
    
    def __init__(
        self,
        config: AuthConfig,
        provider: Optional[AuthProvider] = None
    ):
        self.config = config
        self.provider = provider
        self._roles: Dict[str, Role] = {}
        self._user_roles: Dict[str, List[str]] = {}
    
    def register_role(self, role: Role) -> None:
        """Register a new role."""
        self.roles[role.name] = role
    
    def assign_role(self, user_id: str, role_name: str) -> None:
        """Assign a role to a user."""
        if role_name not in self._roles:
            raise ValueError(f"Role not found: {role_name}")
            
        if user_id not in self._user_roles:
            self._user_roles[user_id] = []
            
        if role_name not in self._user_roles[user_id]:
            self._user_roles[user_id].append(role_name)
    
    async def login(
        self,
        credentials: UserCredentials
    ) -> TokenPair:
        """Authenticate user and generate tokens."""
        if not self.provider:
            raise AuthError("No authentication provider configured")
            
        # Authenticate with provider
        user_data = await self.provider.authenticate(credentials)
        
        # Generate tokens
        access_token = self._generate_token(
            user_data,
            expiration=self.config.token_expiration
        )
        
        refresh_token = self._generate_token(
            user_data,
            expiration=self.config.refresh_token_expiration,
            is_refresh=True
        )
        
        expires_at = datetime.now() + timedelta(
            seconds=self.config.token_expiration
        )
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            token_type=self.config.token_type
        )
    
    async def refresh_token(
        self,
        refresh_token: str
    ) -> TokenPair:
        """Generate new token pair from refresh token."""
        try:
            # Validate refresh token
            payload = jwt.decode(
                refresh_token,
                self.config.secret_key,
                algorithms=[self.config.algorithm]
            )
            
            if not payload.get("refresh"):
                raise AuthError("Invalid refresh token")
                
            # Generate new tokens
            user_data = {
                k: v for k, v in payload.items()
                if k not in ["exp", "refresh"]
            }
            
            return TokenPair(
                access_token=self._generate_token(
                    user_data,
                    expiration=self.config.token_expiration
                ),
                refresh_token=self._generate_token(
                    user_data,
                    expiration=self.config.refresh_token_expiration,
                    is_refresh=True
                ),
                expires_at=datetime.now() + timedelta(
                    seconds=self.config.token_expiration
                ),
                token_type=self.config.token_type
            )
            
        except jwt.InvalidTokenError as e:
            raise AuthError(f"Invalid refresh token: {str(e)}")
    
    def verify_permission(
        self,
        user_id: str,
        resource: str,
        action: str
    ) -> bool:
        """Verify if user has permission for action on resource."""
        user_roles = self._user_roles.get(user_id, [])
        
        for role_name in user_roles:
            role = self._roles[role_name]
            for permission in role.permissions:
                if (permission.resource == resource and 
                    permission.action == action):
                    return True
        
        return False
    
    def _generate_token(
        self,
        data: Dict[str, Any],
        expiration: int,
        is_refresh: bool = False
    ) -> str:
        """Generate JWT token."""
        payload = {
            **data,
            "exp": datetime.now() + timedelta(seconds=expiration)
        }
        
        if is_refresh:
            payload["refresh"] = True
            
        return jwt.encode(
            payload,
            self.config.secret_key,
            algorithm=self.config.algorithm
        )

# Convenience functions
def create_auth_manager(
    secret_key: Optional[str] = None,
    provider: Optional[AuthProvider] = None,
    **kwargs
) -> AuthManager:
    """Create an auth manager instance."""
    config = Config()
    secret_key = secret_key or config.get("AUTH_SECRET_KEY")
    
    if not secret_key:
        raise ValueError("Secret key is required")
        
    auth_config = AuthConfig(secret_key=secret_key, **kwargs)
    return AuthManager(auth_config, provider) 