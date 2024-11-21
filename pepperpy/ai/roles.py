from enum import Enum


class AgentRole(Enum):
    """Agent role enumeration"""

    ANALYST = "analyst"
    DEVELOPER = "developer"
    RESEARCHER = "researcher"
    REVIEWER = "reviewer"
    QA = "qa"
    MANAGER = "manager"
    ARCHITECT = "architect"
    # Add other roles as necessary
