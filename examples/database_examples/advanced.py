import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from pepperpy.core.types import ModuleConfig
from pepperpy.database import DatabaseModule
from pepperpy.database.models import BaseModel


# Define models
class User(BaseModel):
    """User model with authentication and profile information"""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"User(username={self.username}, email={self.email})"


async def main():
    # Configure database
    config = ModuleConfig(
        name="database",
        settings={
            "backend": "postgresql",
            "connection": {
                "url": "postgresql://user:pass@localhost/db",
                "options": {"echo": True},
            },
            "auto_migrate": True,
        },
    )

    # Initialize database
    db = DatabaseModule(config)
    await db.setup()

    try:
        # Create tables
        await db.create_all()

        # Create user
        async with db.session() as session:
            user = User(
                username="john_doe", email="john@example.com", full_name="John Doe"
            )
            session.add(user)
            await session.commit()

        # Query users
        async with db.session() as session:
            # Using query builder
            query = (
                db.query(User)
                .filter_by(username="john_doe")
                .filter(User.is_active == True)  # noqa: E712
                .build()
            )
            result = await session.execute(query)
            user = result.scalar_one()
            print(f"Found user: {user.to_dict()}")

    finally:
        await db.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
