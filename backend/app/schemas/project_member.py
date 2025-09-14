from pydantic import BaseModel, EmailStr
from typing import List

class ProjectMemberInvite(BaseModel):
    email: EmailStr
    roles: List[str]  # e.g. ["member"]

class ProjectMemberOut(BaseModel):
    userId: str
    email: str
    fullName: str
    roles: List[str]