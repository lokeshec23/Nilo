from pydantic import BaseModel, EmailStr

# Used when registering
class UserCreate(BaseModel):
    email: EmailStr
    fullName: str
    password: str

# Used when logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response model
class UserOut(BaseModel):
    id: str
    email: EmailStr
    fullName: str
    isActive: bool
