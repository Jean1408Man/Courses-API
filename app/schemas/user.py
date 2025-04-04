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

    class Config:
        orm_mode = True

class UserRead(UserBase):
    id: int
    courses: List[CourseInUser] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    email: str
    password: str
