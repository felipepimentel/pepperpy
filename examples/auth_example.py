"""Example of authentication and authorization."""
import asyncio
from pepperpy.auth import (
    create_auth_manager,
    UserCredentials,
    Permission,
    Role,
    AuthProvider,
    AuthError
)

class DemoAuthProvider(AuthProvider):
    """Demo authentication provider."""
    
    async def authenticate(self, credentials: UserCredentials) -> dict:
        """Simulate authentication."""
        if credentials.username == "admin" and credentials.password == "secret":
            return {
                "user_id": "1",
                "username": credentials.username,
                "email": "admin@example.com"
            }
        raise AuthError("Invalid credentials")
    
    async def validate_token(self, token: str) -> dict:
        """Validate token."""
        # In a real implementation, validate token with your auth service
        return {"valid": True}

async def demonstrate_auth():
    """Demonstrate auth functionality."""
    # Create auth manager
    auth = create_auth_manager(
        secret_key="your-secret-key",
        provider=DemoAuthProvider()
    )
    
    # Define permissions
    view_users = Permission(
        name="view_users",
        description="Can view users",
        resource="users",
        action="view"
    )
    
    edit_users = Permission(
        name="edit_users",
        description="Can edit users",
        resource="users",
        action="edit"
    )
    
    # Define roles
    admin_role = Role(
        name="admin",
        description="Administrator",
        permissions=[view_users, edit_users]
    )
    
    viewer_role = Role(
        name="viewer",
        description="Viewer",
        permissions=[view_users]
    )
    
    # Register roles
    auth.register_role(admin_role)
    auth.register_role(viewer_role)
    
    try:
        # Login
        credentials = UserCredentials(
            username="admin",
            password="secret"
        )
        
        tokens = await auth.login(credentials)
        print(f"Access Token: {tokens.access_token}")
        print(f"Refresh Token: {tokens.refresh_token}")
        print(f"Expires at: {tokens.expires_at}")
        
        # Assign role
        auth.assign_role("1", "admin")
        
        # Check permissions
        can_view = auth.verify_permission("1", "users", "view")
        can_edit = auth.verify_permission("1", "users", "edit")
        
        print(f"\nPermissions for user 1:")
        print(f"Can view users: {can_view}")
        print(f"Can edit users: {can_edit}")
        
        # Refresh tokens
        new_tokens = await auth.refresh_token(tokens.refresh_token)
        print(f"\nNew Access Token: {new_tokens.access_token}")
        
    except AuthError as e:
        print(f"Authentication error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(demonstrate_auth()) 