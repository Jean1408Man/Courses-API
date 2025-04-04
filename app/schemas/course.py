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

    model_config = {
        "from_attributes": True
    }

class CourseRead(CourseBase):
    id: int
    users: List[UserInCourse] = []

    model_config = {
        "from_attributes": True
    }

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
