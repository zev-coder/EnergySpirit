from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from App.DB.db import create_db_and_tables, get_async_session
from App.DB.dependencies.User.router import router
from App.DB.dependencies.User.scheme import RolesScheme
from App.DB.model import Roles
from App.middleware.CORS import setup_cors


# Async mecahnism, to support application based asyncio
@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_FILE = Path("database.db")
    if not DB_FILE.exists():
        print("Database not found. Creating...")
        await create_db_and_tables()
    else:
        print("Database already exists.")
    yield

# MainApp, the heart of application
app = FastAPI(lifespan=lifespan)
setup_cors(app)

# Calling available services
app.include_router(router)

# Roles Payload, to create a role
@app.post("/roles")
async def create_role(
    payload: RolesScheme,
    db: AsyncSession = Depends(get_async_session)
):
    role = Roles(**payload.model_dump())

    db.add(role)
    await db.commit()
    await db.refresh(role)

    return role

# Testing, just testing
@app.get('/')
def test():
    return {'test' : 'test'}
