from contextlib import asynccontextmanager
from pathlib import Path
import uuid
from fastapi import Depends, FastAPI, HTTPException,status,Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from App.DB.db import create_db_and_tables, get_async_session, get_user_db
from App.DB.dependencies.Product.products import CreateProduct, ProductResponses
from App.DB.dependencies.User.router import router
from App.DB.dependencies.Roles.roles import RolesCreate, RolesResponse
from App.DB.dependencies.Order.order import OrderRead, OrderUpdate
from App.DB.model import Order, Product, Roles, OrderStatus, User
from App.middleware.CORS import setup_cors
from sqlalchemy import Select, delete, select
from sqlalchemy.exc import IntegrityError
from App.middleware.logger.logging import logger
from App.middleware.logger.logging import log_auth_requests
from App.DB.dependencies.User.user import current_active_user


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
@app.post("/create_roles", response_model=RolesResponse)
async def create_role(
    payload: RolesCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        role_name = await db.scalar(
            select(Roles.roles_name).where(Roles.id == user.role_id)
        )

        if role_name != "MODERATOR":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

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
@app.get('/roles-all', response_model=RolesResponse)
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
@app.get('/roles/{roles_id}', response_model=list[RolesResponse])
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
@app.get('/product', response_model=list[ProductResponses])
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
@app.post('/create-product')
async def create_product(
    payload: CreateProduct,
    photo: UploadFile,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    try:

        role_name = await session.scalar(
            select(Roles.roles_name).where(Roles.id == user.role_id)
        )

        if role_name != "MODERATOR":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

        allowed_photo = {
            "image/jpg",
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if photo.content_type not in allowed_photo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='must be an image'
            )

        filename = f"{uuid.uuid4()}_photo.filename"
        file_path = f'uploads/{filename}'

        with open(file_path, 'wb') as file:
            file.write(await photo.read())

        create = Product(
            name=payload.name,
            description=payload.description,
            created_by= user.id,
            price = payload.price,
            image=file_path,
        )

        session.add(create)

        await session.commit()
        await session.refresh(create)

        return create

    except HTTPException:
        raise

    except:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


#deleting product
@app.delete("/delete-product/{product_id}", response_model=ProductResponses)
async def delete_product(
    product_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        result = await session.execute(
            select(Product).where(Product.name == product_id)
        )

        product = result.scalar_one_or_none()


        if product is None:
            all_names = (await session.execute(select(Product.name))).scalars().all()
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="didn't match with available product")

        await session.delete(product)
        await session.commit()

        return product
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='internal server error'
        )


#reading chart responses
@app.get('/chart')
async def get_chart(
    payload: OrderRead,
    session: AsyncSession = Depends(get_async_session),
    page:int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100)
):
    cart = await session.execute(Select(Order))

    return cart


#making cart
@app.post('/order')
async def create_order(
    payload: OrderUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    # Cari product
    result = await session.execute(
        select(Product).where(Product.id == payload.product_id))

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product tidak ditemukan"
        )

    # Convert payload → dict
    data = payload.model_dump()

    # Masukkan hasil query ke payload
    data["product_id"] = product.id
    data["total_amount"] = product.price
    data["status"] = OrderStatus.PENDING

    # Buat entity Order
    order = Order(**data)

    session.add(order)

    await session.commit()
    await session.refresh(order)

    return order

@app.post('/order/purchase')
async def purchase_item(
    payload: OrderUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    data = payload.model_dump()
    confirmed = OrderStatus.CONFIRMED

    order = await session.execute(
        select(Order).where(Order.id == data['id'])
    )

    order_result = order.scalar_one_or_none()

    if order_result.status == 'pending': #type: ignore
        data['status'] = confirmed
        data_entity = Order(**data)

        #stripe logic state

    session.add(data)

    await session.commit()
    await session.refresh(data)

    return data
