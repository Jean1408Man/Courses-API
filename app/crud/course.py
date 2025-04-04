from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.schemas.course import CourseCreate
from app.models.base import Course


async def get_course(db: AsyncSession, course_id: int):
    result = await db.execute(
        select(Course).options(selectinload(Course.users)).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


async def get_courses(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Course).options(selectinload(Course.users)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_course(db: AsyncSession, course: CourseCreate):
    db_course = Course(
        title=course.title,
        description=course.description
    )
    db.add(db_course)
    try:
        await db.commit()
        result = await db.execute(
            select(Course).options(selectinload(Course.users)).where(Course.id == db_course.id)
        )
        return result.scalar_one()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Course already exists or data conflict")


async def delete_course(db: AsyncSession, course_id: int):
    course = await get_course(db, course_id)
    await db.delete(course)
    await db.commit()
    return course


async def update_course(db: AsyncSession, course_id: int, new_data: dict):
    course = await get_course(db, course_id)
    for key, value in new_data.items():
        setattr(course, key, value)
    try:
        await db.commit()
        result = await db.execute(
            select(Course).options(selectinload(Course.users)).where(Course.id == course.id)
        )
        return result.scalar_one()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to data conflict")
