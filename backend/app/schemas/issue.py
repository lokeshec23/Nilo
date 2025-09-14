from pydantic import BaseModel
from typing import Optional, List, Dict

class IssueCreate(BaseModel):
    projectId: str
    summary: str
    description: Optional[str] = None
    assigneeId: Optional[str] = None
    priority: str = "Medium"
    labels: List[str] = []
    customFields: Dict[str, str] = {}

class IssueOut(BaseModel):
    id: str
    projectId: str
    key: str
    summary: str
    description: Optional[str]
    status: str
    assigneeId: Optional[str]
    priority: str
    labels: List[str]
    customFields: Dict[str, str]
