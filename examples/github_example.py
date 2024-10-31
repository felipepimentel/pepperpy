"""Example of GitHub operations."""
from pepperpy.github import GitHubManager, WorkflowManager, ActionsManager, SecretsManager
from pepperpy.github.core import GitHubConfig, WorkflowConfig

async def demonstrate_github():
    # Configuração
    config = GitHubConfig(token="your_github_token")
    github = GitHubManager(config)
    
    # Criar workflow de CI
    workflow_manager = WorkflowManager(github)
    ci_workflow = WorkflowConfig(
        name="CI Pipeline",
        on=["push", "pull_request"],
        jobs={
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "uses": "actions/checkout@v3"
                    },
                    {
                        "name": "Set up Python",
                        "uses": "actions/setup-python@v4",
                        "with": {
                            "python-version": "3.10"
                        }
                    },
                    {
                        "name": "Install dependencies",
                        "run": "pip install poetry && poetry install"
                    },
                    {
                        "name": "Run tests",
                        "run": "poetry run pytest"
                    }
                ]
            }
        }
    )
    
    await workflow_manager.create_workflow("owner/repo", ci_workflow)
    
    # Listar workflows
    workflows = await workflow_manager.list_workflows("owner/repo")
    print("Workflows:", workflows)
    
    # Gerenciar Actions
    actions = ActionsManager(github)
    
    # Listar runs recentes
    runs = await actions.list_runs(
        "owner/repo",
        status="completed",
        branch="main"
    )
    print("Recent runs:", runs)
    
    # Gerenciar secrets
    secrets = SecretsManager(github)
    await secrets.set_secret(
        "owner/repo",
        "API_KEY",
        "secret_value",
        visibility="private"
    )
    
    secret_names = await secrets.list_secrets("owner/repo")
    print("Repository secrets:", secret_names)

if __name__ == "__main__":
    import asyncio
    asyncio.run(demonstrate_github()) 