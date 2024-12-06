"""Script to reorganize project structure"""
import os
import shutil
from pathlib import Path

MOVES = {
    # Docker
    "docker-compose.yml": "tools/docker/docker-compose.yml",
    "Dockerfile": "tools/docker/Dockerfile",
    
    # CI/CD
    "noxfile.py": "tools/ci/noxfile.py",
    
    # Docs
    "mkdocs.yml": "tools/docs/mkdocs.yml",
    
    # Config
    "pyrightconfig.json": "tools/config/pyrightconfig.json",
    ".project-root": "tools/config/project-root",
    
    # Templates
    "CHANGELOG.md.template": "tools/templates/CHANGELOG.md.template",
    ".env.template": "tools/templates/.env.template",
    
    # Monitoring
    "prometheus.yml": "tools/monitoring/prometheus.yml",
    
    # Scripts (mantendo os moves anteriores)
    "scripts/build.py": "tools/scripts/build.py",
    "scripts/replace_path_deps.sh": "tools/scripts/replace_path_deps.sh",
    "scripts/poetry_lock_no_update.sh": "tools/scripts/poetry_lock_no_update.sh",
    "scripts/poetry_lock_update.sh": "tools/scripts/poetry_lock_update.sh",
    "scripts/poetry_install.sh": "tools/scripts/poetry_install.sh",
    "scripts/projects.sh": "tools/scripts/projects.sh",
    "scripts/manage_deps.py": "tools/dev/manage_deps.py",
    "scripts/migrate.py": "tools/scripts/migrate.py",
    "scripts/validate_migration.py": "tools/scripts/validate_migration.py",
    "scripts/lint.py": "tools/lint/lint.py",
}

REMOVE = [
    "poetry copy.toml",
]

# Arquivos que precisam de symlinks
SYMLINKS = {
    "tools/ci/noxfile.py": "noxfile.py",
    "tools/docker/docker-compose.yml": "docker-compose.yml",
}

def create_symlink(src: Path, dest: Path) -> None:
    """Create a symlink and handle Windows/Unix differences"""
    try:
        if os.name == 'nt':  # Windows
            import subprocess
            subprocess.run(['mklink', str(dest), str(src)], shell=True, check=True)
        else:  # Unix
            os.symlink(src, dest)
    except Exception as e:
        print(f"Warning: Could not create symlink {dest} -> {src}: {e}")

def main():
    """Execute reorganization"""
    root = Path(".")
    
    # Create necessary directories
    dirs = {Path(dest).parent for dest in MOVES.values()}
    for dir_path in dirs:
        (root / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Move files
    for src, dest in MOVES.items():
        src_path = root / src
        dest_path = root / dest
        if src_path.exists():
            print(f"Moving {src} to {dest}")
            shutil.move(str(src_path), str(dest_path))
            
            # Create symlink if needed
            if dest in SYMLINKS:
                create_symlink(dest_path, root / SYMLINKS[dest])
    
    # Remove redundant files
    for file in REMOVE:
        path = root / file
        if path.exists():
            print(f"Removing {file}")
            path.unlink()
    
    print("Project structure reorganized successfully!")

if __name__ == "__main__":
    main() 