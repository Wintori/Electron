from typing import Optional, List

from fastapi import APIRouter, status, Request
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update

from back.app.models import Group
from back.app.models.users import Users

from back.app.schems.users import UserResponse, UpdateUserRequest, CreateUserRequest
from back.app.utils.items.utils import get_or_404

router = APIRouter(
    prefix="/ds",
    tags=["User CRUD + List"],
)


@router.post(
    "/create_user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
        request: Request,
        model: CreateUserRequest,

):
    async with request.app.state.db.get_session() as session:
        await get_or_404(session, Group, model.group_id)
        query = sa_insert(Users).values(**model.dict()).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()
        print(result)
        await session.commit()

    return result


@router.get(
    "/get_user/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_data(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        result = await get_or_404(session, Users, id)
    return result


@router.get(
    "/get_api_keys",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
)
async def get_list(
        request: Request,
):
    async with request.app.state.db.get_session() as session:
        result = (await session.execute(
            select(Users).group_by(Users.group_id)
        )).scalars().all()
    return result


@router.patch(
    "/update_api_keys/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def update_user(
        request: Request,
        model: UpdateUserRequest,
        id: int
):
    data = dict()

    for key, value in model.dict().items():
        if model.dict()[key] is not None:
            data[key] = value

    async with request.app.state.db.get_session() as session:
        if model.group_id is not None:
            await get_or_404(session, Group, model.group_id)
        await get_or_404(session, Users, id)
        query = sa_update(Users).where(Users.id == id).values(**data).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()

    return result


@router.delete(
    "/delete_api_keys/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        await get_or_404(session, Users, id)
        query = sa_delete(Users).where(Users.id == id)
        await session.execute(query)
