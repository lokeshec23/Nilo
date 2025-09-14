from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: str
    issueId: str
    userId: str
    body: str
    createdAt: datetime
