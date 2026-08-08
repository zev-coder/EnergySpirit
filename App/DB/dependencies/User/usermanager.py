from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
import uuid
from App.DB.db import get_async_session, get_user_db
from App.DB.dependencies.User.scheme import UserCreate
from App.middleware.logger.logging import setup_auth_logging
from App.DB.model import User
from sqlalchemy.ext.asyncio import AsyncSession
from App.DB.model import Roles
from sqlalchemy import select

SECRET = "SECRET"
auth_logger = setup_auth_logging()

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):

    def __init__(self, user_db, session: AsyncSession):
        super.__init__(user_db)
        self.session = session

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
    self,
    user_create: UserCreate,
    safe: bool = False,
    request: Request | None = None
    ):
        role = await self.session.scalar(
            select(Roles).where(
                Roles.id == user_create.roles_id
            )
        )

        if role is None:
            raise HTTPException(
                status_code=404,
                detail="Role tidak ditemukan"
            )

        user = await super().create(
            user_create,
            safe=safe,
            request=request
        )

        user.role_id = role.id

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def on_after_register(self, user: User, request: Request | None = None):
        auth_logger.info("user_registered", extra={"user_id": user.id, "email": user.email})

    async def on_after_login(self, user: User, request: Request | None = None, response=None):
        auth_logger.info("user_login_success", extra={"user_id": user.id, "email": user.email})

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        auth_logger.info("password_reset_requested", extra={"user_id": user.id, "email": user.email})

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        auth_logger.info("verification_requested", extra={"user_id": user.id, "email": user.email})

    async def on_after_reset_password(self, user: User, request: Request | None = None):
        auth_logger.info("password_reset_done", extra={"user_id": user.id, "email": user.email})

    async def on_after_verify(self, user: User, request: Request | None = None):
        auth_logger.info("user_verified", extra={"user_id": user.id, "email": user.email})

async def get_user_manager(
        user_db=Depends(get_user_db),
        session: AsyncSession = Depends(get_async_session)
        ):
    yield UserManager(user_db, session)

