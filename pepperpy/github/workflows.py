"""GitHub Actions workflow management."""
from typing import Dict, List, Optional, Union
import yaml
from pathlib import Path

from .core import GitHubManager, WorkflowConfig

class WorkflowManager:
    """Manage GitHub Actions workflows."""
    
    def __init__(self, github: GitHubManager):
        self.github = github
        
    async def create_workflow(
        self,
        repo: str,
        config: WorkflowConfig,
        path: Optional[str] = None
    ) -> None:
        """Create or update a workflow."""
        repository = await self.github.get_repository(repo)
        
        workflow_path = path or f".github/workflows/{config.name.lower().replace(' ', '_')}.yml"
        workflow_content = yaml.safe_dump({
            "name": config.name,
            "on": config.on,
            "jobs": config.jobs,
            **({"env": config.env} if config.env else {})
        })
        
        try:
            # Update if exists
            file = repository.get_contents(workflow_path)
            repository.update_file(
                workflow_path,
                f"Update workflow: {config.name}",
                workflow_content,
                file.sha
            )
        except:
            # Create if doesn't exist
            repository.create_file(
                workflow_path,
                f"Create workflow: {config.name}",
                workflow_content
            )
            
    async def list_workflows(self, repo: str) -> List[Dict]:
        """List all workflows in a repository."""
        repository = await self.github.get_repository(repo)
        return [
            {
                "id": workflow.id,
                "name": workflow.name,
                "path": workflow.path,
                "state": workflow.state,
                "created_at": workflow.created_at,
                "updated_at": workflow.updated_at
            }
            for workflow in repository.get_workflows()
        ]
        
    async def trigger_workflow(
        self,
        repo: str,
        workflow_id: Union[int, str],
        ref: str = "main",
        inputs: Optional[Dict] = None
    ) -> None:
        """Trigger a workflow run."""
        repository = await self.github.get_repository(repo)
        workflow = repository.get_workflow(workflow_id)
        workflow.create_dispatch(ref, inputs or {}) 