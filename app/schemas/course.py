from pydantic import BaseModel
from typing import List, Optional

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class UserInCourse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class CourseRead(CourseBase):
    id: int
    users: List[UserInCourse] = []

    class Config:
        orm_mode = True
