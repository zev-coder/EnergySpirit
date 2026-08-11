from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException,status,Query
from sqlalchemy.ext.asyncio import AsyncSession
from App.DB.db import create_db_and_tables, get_async_session, get_user_db
from App.DB.dependencies.Product.products import CreateProduct, ProductResponses
from App.DB.dependencies.User.router import router
from App.DB.dependencies.Roles.roles import RolesCreate, RolesResponse
from App.DB.model import Product, Roles
from App.middleware.CORS import setup_cors
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from App.middleware.logger.logging import logger
from App.middleware.logger.logging import log_auth_requests


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

#middleware
app.middleware("http")(log_auth_requests)

# Roles Payload, to create a role
@app.post("/create_roles")
async def create_role(
    payload: RolesCreate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        role = Roles(**payload.model_dump())

        db.add(role)
        await db.commit()
        await db.refresh(role)

        return role
    except IntegrityError as e:
        await db.rollback()
        logger.exception(e)

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role sudah tersedia"
            )

    except Exception as e:
        await db.rollback()
        logger.exception(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server sedang bermasalah"
        )

# Getting all roles within 5
@app.get('roles-all', response_model=RolesResponse)
async def get_roles_all(
        db: AsyncSession = Depends(get_async_session),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
    ):
        try:
            get_role =  await db.execute(
                select(Roles)
                .offset(page).
                limit(limit)
            )
            result = get_role.scalars().all()
            return result

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Not Found"
            )

        except Exception as e:
            logger.exception(e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server sedang bermasalah"
            )


# Getting specific roles within 5
@app.get('/roles/{roles_id}', response_model=RolesResponse)
async def get_roles(
    roles_name: str,
    db: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    try:
        get_role =  await db.execute(
            select(Roles)
            .offset(page).
            limit(limit)
            .where(Roles.roles_name == roles_name)
        )

        result = get_role.scalars().all()

        return result

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )

    except Exception as e:

        logger.exception(e)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server sedang bermasalah"
        )


#getting the list of product
@app.get('product/', response_model=ProductResponses)
async def product_query(
    session: AsyncSession = Depends(get_async_session),
    page:int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100)
):
    query = await session.execute(
        select(Product)
        .offset(page)
        .limit(limit)
    )

    result = query.scalars().all()

    return result


#creating a product
# @app.post('create-product/')
# async def create_product(
#     payload: CreateProduct,
#     name: str,
#     description: str,
#     session: AsyncSession = Depends(get_async_session),
#     user: AsyncSession = Depends(get_user_db)
# ):
#     try:
#         create = Product(
#             name=name,
#             description=description,
#             created_by=user
#         )
#     except:
#         pass
