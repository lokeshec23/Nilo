from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HistoryOut(BaseModel):
    id: str
    issueId: str
    changedBy: str
    field: str
    fromValue: Optional[str]
    toValue: Optional[str]
    createdAt: datetime
