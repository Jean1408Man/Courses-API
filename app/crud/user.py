from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.schemas.user import UserCreate
from app.models.base import User
from passlib.context import CryptContext
from app.core.security import verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).options(selectinload(User.courses)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).options(selectinload(User.courses)).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(User).options(selectinload(User.courses)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    try:
        await db.commit()
        result = await db.execute(
            select(User).options(selectinload(User.courses)).where(User.id == db_user.id)
        )
        return result.scalar_one()
    except IntegrityError as e:
        await db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=400, detail="Email o usuario ya registrado")


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True



async def update_user(db: AsyncSession, user_id: int, new_data: dict):
    user = await get_user(db, user_id)
    for key, value in new_data.items():
        setattr(user, key, value)
    try:
        await db.commit()
        # Recargar el usuario con cursos después del update
        result = await db.execute(
            select(User).options(selectinload(User.courses)).where(User.id == user.id)
        )
        return result.scalar_one()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to data conflict")


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
