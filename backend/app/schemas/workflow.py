from pydantic import BaseModel
from typing import List, Dict

class WorkflowCreate(BaseModel):
    name: str
    statuses: List[str]
    transitions: Dict[str, List[str]]  # e.g. { "To Do": ["In Progress"], "In Progress": ["Done"] }

class WorkflowOut(WorkflowCreate):
    id: str
