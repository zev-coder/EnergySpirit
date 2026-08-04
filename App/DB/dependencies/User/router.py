from fastapi import APIRouter
from App.DB.dependencies.User.user import fastapi_users, auth_backend
from App.DB.dependencies.User.scheme import (
    UserRead,
    UserCreate,
    UserUpdate,
)

router = APIRouter(prefix="/auth", tags=["auth"])


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

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
