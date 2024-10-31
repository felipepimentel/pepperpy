"""Database migration system."""
from typing import List, Optional
from pathlib import Path
import importlib.util
import asyncio
from datetime import datetime

class Migration:
    """Base class for migrations."""
    
    def __init__(self, version: str, description: str):
        self.version = version
        self.description = description
        
    async def up(self, connection):
        """Apply migration."""
        raise NotImplementedError()
        
    async def down(self, connection):
        """Revert migration."""
        raise NotImplementedError()

class MigrationManager:
    """Manage database migrations."""
    
    def __init__(self, db_connection, migrations_dir: str = "migrations"):
        self.connection = db_connection
        self.migrations_dir = Path(migrations_dir)
        self.migrations: List[Migration] = []
        
    async def init(self):
        """Initialize migrations table."""
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                version VARCHAR(50) PRIMARY KEY,
                description TEXT,
                applied_at TIMESTAMP
            )
        """)
        
    def load_migrations(self):
        """Load migration files."""
        self.migrations = []
        for file in sorted(self.migrations_dir.glob("*.py")):
            if file.stem.startswith("_"):
                continue
                
            spec = importlib.util.spec_from_file_location(
                f"migration_{file.stem}", file
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "Migration"):
                self.migrations.append(module.Migration())
                
    async def get_applied_versions(self) -> List[str]:
        """Get list of applied migrations."""
        result = await self.connection.fetch(
            "SELECT version FROM migrations ORDER BY version"
        )
        return [row["version"] for row in result]
        
    async def migrate(self, target_version: Optional[str] = None):
        """Apply pending migrations."""
        await self.init()
        self.load_migrations()
        
        applied = await self.get_applied_versions()
        pending = [m for m in self.migrations if m.version not in applied]
        
        if target_version:
            pending = [m for m in pending if m.version <= target_version]
            
        for migration in pending:
            try:
                await migration.up(self.connection)
                await self.connection.execute(
                    """
                    INSERT INTO migrations (version, description, applied_at)
                    VALUES ($1, $2, $3)
                    """,
                    migration.version,
                    migration.description,
                    datetime.now()
                )
                print(f"Applied migration {migration.version}")
            except Exception as e:
                print(f"Error applying migration {migration.version}: {e}")
                raise 