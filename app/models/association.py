from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.database import Base

user_course = Table(
    "user_course",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"))
)
