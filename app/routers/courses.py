from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.course import CourseRead, CourseCreate, CourseUpdate
from app.models.user import User as UserModel
from app.models.base import Course
from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.crud import course as course_crud
from app.models.association import user_course
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.get("/", response_model=List[CourseRead])
async def get_all_courses(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await course_crud.get_courses(db)


@router.get("/me", response_model=List[CourseRead])
async def get_my_courses(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(
        select(Course)
        .join(user_course, Course.id == user_course.c.course_id)
        .where(user_course.c.user_id == current_user.id)
        .options(selectinload(Course.users))
    )
    return result.scalars().all()

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await course_crud.create_course(db, course_data)


@router.get("/{course_id}", response_model=CourseRead)
async def get_course_by_id(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await course_crud.get_course(db, course_id)


@router.put("/{course_id}", response_model=CourseRead)
async def update_course_by_id(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await course_crud.update_course(db, course_id, course_update.dict(exclude_unset=True))


@router.delete("/{course_id}", response_model=CourseRead)
async def delete_course_by_id(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await course_crud.delete_course(db, course_id)


@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
async def enroll_in_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    course = await course_crud.get_course(db, course_id)

    # Verificar si ya está inscrito
    result = await db.execute(
        select(user_course).where(
            user_course.c.user_id == current_user.id,
            user_course.c.course_id == course.id
        )
    )
    existing = result.first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso")

    # Inscribir
    await db.execute(user_course.insert().values(user_id=current_user.id, course_id=course.id))
    await db.commit()
    return {"message": f"Inscrito en el curso {course.title}"}
