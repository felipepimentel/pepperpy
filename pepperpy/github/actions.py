"""GitHub Actions management."""
from typing import Dict, List, Optional, Union
from datetime import datetime

from .core import GitHubManager

class ActionsManager:
    """Manage GitHub Actions."""
    
    def __init__(self, github: GitHubManager):
        self.github = github
        
    async def list_runs(
        self,
        repo: str,
        workflow_id: Optional[Union[int, str]] = None,
        status: Optional[str] = None,
        branch: Optional[str] = None
    ) -> List[Dict]:
        """List workflow runs."""
        repository = await self.github.get_repository(repo)
        
        filters = {}
        if status:
            filters["status"] = status
        if branch:
            filters["branch"] = branch
            
        if workflow_id:
            workflow = repository.get_workflow(workflow_id)
            runs = workflow.get_runs(**filters)
        else:
            runs = repository.get_workflow_runs(**filters)
            
        return [
            {
                "id": run.id,
                "name": run.name,
                "status": run.status,
                "conclusion": run.conclusion,
                "branch": run.head_branch,
                "commit": run.head_sha,
                "url": run.html_url,
                "created_at": run.created_at,
                "updated_at": run.updated_at
            }
            for run in runs
        ]
        
    async def cancel_run(self, repo: str, run_id: int) -> None:
        """Cancel a workflow run."""
        repository = await self.github.get_repository(repo)
        run = repository.get_workflow_run(run_id)
        run.cancel()
        
    async def rerun_workflow(self, repo: str, run_id: int) -> None:
        """Rerun a workflow."""
        repository = await self.github.get_repository(repo)
        run = repository.get_workflow_run(run_id)
        run.rerun()
        
    async def get_run_logs(self, repo: str, run_id: int) -> str:
        """Get logs from a workflow run."""
        repository = await self.github.get_repository(repo)
        run = repository.get_workflow_run(run_id)
        return run.get_logs() 