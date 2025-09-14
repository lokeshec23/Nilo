from pydantic import BaseModel
from datetime import datetime

class NotificationOut(BaseModel):
    id: str
    userId: str
    issueId: str
    message: str
    createdAt: datetime
    read: bool
