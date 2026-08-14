import email

from argon2 import hash_password
from fastapi import APIRouter, HTTPException
from fastapi_users import password
from App.DB.db import get_async_session
from App.DB.dependencies.User.user import fastapi_users, auth_backend
from App.DB.dependencies.User.scheme import (
    UserRead,
    UserCreate,
    UserUpdate,
)
from sqlalchemy.ext.asyncio  import AsyncSession
from fastapi import Depends
from sqlalchemy import select
from App.DB.model import Roles, User

router = APIRouter(prefix="/auth", tags=["auth"])


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

@router.post('/auth/register')
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):

    #password hasher
    from argon2 import PasswordHasher
    ph = PasswordHasher()

    role = await db.scalar(
        select(Roles)
        .where(Roles.id == payload.roles_id)
    )

    if role is None:
        HTTPException(
            status_code=404,
            detail='role tidak ditemukan'
        )
    user = User(
        username=payload.username,
        hashed_password= ph.hash(payload.password), #hashing password
        role_id=payload.roles_id,
        email = payload.email,
        is_active = payload.is_active,
        is_superuser = payload.is_superuser,
        is_verified = payload.is_verified
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/verify",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)
