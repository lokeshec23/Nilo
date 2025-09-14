from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SprintCreate(BaseModel):
    name: str
    goal: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None

class SprintOut(SprintCreate):
    id: str
    projectId: str
    status: str   # planned, active, completed
    issues: List[str] = []
