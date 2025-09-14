from pydantic import BaseModel
from typing import Optional

class ProjectCreate(BaseModel):
    key: str
    name: str
    description: Optional[str] = None

class ProjectOut(BaseModel):
    id: str
    key: str
    name: str
    description: Optional[str] = None
    orgId: str
