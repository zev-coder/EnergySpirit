import os
import uuid
from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from App.DB.db import get_async_session, get_user_db
from App.DB.dependencies.User.scheme import UserCreate
from App.DB.model import Roles, User
from App.middleware.logger.logging import setup_auth_logging

SECRET = os.environ['EFVMKEDSCDKEOQV']
auth_logger = setup_auth_logging()

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):

    def __init__(self, user_db, session: AsyncSession):
        self.session = session
        super().__init__(user_db)

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Request | None = None
    ):
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        role = await self.session.scalar(
            select(Roles).where(Roles.roles_name == "ADMIN")
        )
        if role is None:
            raise HTTPException(
                status_code=404,
                detail="Role default user belum tersedia"
            )

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = role.id

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)

        return created_user

    async def authenticate(self, credentials):
        identifier = credentials.username

        # Coba cari berdasarkan email
        user = await self.user_db.get_by_email(identifier)

        # Kalau bukan email, cari berdasarkan username
        if user is None:
            result = await self.session.execute(
                select(User).where(
                    User.username == identifier
                )
            )

            user = result.scalar_one_or_none()

        if user is None:
            return None

        verified, updated_password_hash = (
            self.password_helper.verify_and_update(
                credentials.password,
                user.hashed_password
            )
        )

        if not verified:
            return None

        if updated_password_hash is not None:
            user.hashed_password = updated_password_hash
            await self.session.commit()

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
