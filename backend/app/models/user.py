from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: Optional[str]  # store ObjectId as string
    email: EmailStr
    fullName: str
    passwordHash: str
    isActive: bool = True
    globalPermissions: list[str] = []
