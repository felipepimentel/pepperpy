"""GitHub operations manager."""
from typing import Dict, List, Optional, Union
from pathlib import Path
import base64
from datetime import datetime

from github import Github, GithubIntegration
from github.Repository import Repository
from github.Workflow import Workflow
from github.WorkflowRun import WorkflowRun
from pydantic import BaseModel, Field

class GitHubConfig(BaseModel):
    """GitHub configuration settings."""
    token: Optional[str] = Field(None, description="Personal access token")
    app_id: Optional[int] = Field(None, description="GitHub App ID")
    private_key: Optional[str] = Field(None, description="GitHub App private key")
    base_url: Optional[str] = Field(None, description="GitHub API URL for enterprise")
    
class WorkflowConfig(BaseModel):
    """Workflow configuration."""
    name: str
    on: Union[str, List[str], Dict]
    jobs: Dict
    env: Optional[Dict] = None

class GitHubManager:
    """Manage GitHub operations."""
    
    def __init__(self, config: Optional[GitHubConfig] = None):
        self.config = config or GitHubConfig()
        
        if self.config.token:
            self.client = Github(self.config.token, base_url=self.config.base_url)
        elif self.config.app_id and self.config.private_key:
            integration = GithubIntegration(
                self.config.app_id,
                self.config.private_key,
                base_url=self.config.base_url
            )
            self.client = integration.get_github_for_installation()
        else:
            raise ValueError("Either token or app credentials required")
            
    async def create_repository(
        self,
        name: str,
        private: bool = False,
        description: Optional[str] = None,
        **kwargs
    ) -> Repository:
        """Create a new repository."""
        return self.client.get_user().create_repo(
            name=name,
            private=private,
            description=description,
            **kwargs
        )
    
    async def get_repository(self, full_name: str) -> Repository:
        """Get repository by full name (owner/repo)."""
        return self.client.get_repo(full_name)