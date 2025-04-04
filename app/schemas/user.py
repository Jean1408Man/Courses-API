from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class CourseInUser(BaseModel):
    id: int
    title: str

    model_config = {
        "from_attributes": True
    }

class UserRead(UserBase):
    id: int
    courses: List[CourseInUser] = []

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    model_config = {
        "from_attributes": True
    }