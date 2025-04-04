from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.user import UserRead, UserUpdate
from app.models.user import User as UserModel
from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.crud import user as user_crud

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserRead)
async def read_own_profile(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user(db, user_id=current_user.id)
    return user

@router.get("/", response_model=List[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await user_crud.get_users(db)

@router.get("/{user_id}", response_model=UserRead)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await user_crud.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Comentar para evitar autenticar constantemente
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para actualizar este usuario")

    updated_user = await user_crud.update_user(db, user_id, user_update.dict(exclude_unset=True))
    return updated_user
