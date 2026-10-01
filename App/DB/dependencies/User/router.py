from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from App.DB.db import get_async_session
from App.DB.dependencies.User.user import (
    auth_backend,
    current_active_user,
    current_superuser,
    fastapi_users,
)
from App.DB.dependencies.User.scheme import (
    UserRead,
    UserCreate,
    UserUpdate,
)
from sqlalchemy.ext.asyncio  import AsyncSession
from App.DB.model import User
from App.DB.dependencies.User.usermanager import get_user_manager


router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

@router.patch("/change-username")
async def change_username(
    payload: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    user.username = payload.username

    await session.commit()
    await session.refresh(user)

    return {
        "message": "Username berhasil diubah"
    }

@router.post("/register", response_model=UserRead, status_code=201)
async def create_user(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    username: Annotated[str, Form()] = " ",
    photo: Annotated[UploadFile | None, File()] = None,
    user_manager=Depends(get_user_manager),
):
    payload = UserCreate(email=email, password=password, username=username)
    created_user = await user_manager.create(
        photo=photo,
        user_create=payload,
        safe=True,
        request=request,
    )
    return UserRead.model_validate(created_user)

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
