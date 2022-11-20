from typing import Optional, List

from fastapi import APIRouter, status, Request
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update
from sqlalchemy.orm import joinedload

from back.app.models.group import Group

from back.app.schems.group import GroupResponse, UpdateGroupRequest, CreateGroupRequest, GroupData
from back.app.utils.items.utils import get_or_404

router = APIRouter(
    prefix="/group",
    tags=["Group CRUD + List"],
)


@router.post(
    "/create_group",
    status_code=status.HTTP_201_CREATED,
    response_model=GroupData,
)
async def create_folder(
        request: Request,
        model: CreateGroupRequest,

):
    async with request.app.state.db.get_session() as session:
        query = sa_insert(Group).values(**model.dict()).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()
        await session.commit()

    return result


@router.get(
    "/get_group/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GroupResponse,
)
async def get_data(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        query = select(Group).where(Group.id == id).options(joinedload(Group.users))
        (await session.execute(query)).mappings().first()

        result = await get_or_404(session, Group, id)

    return result


@router.get(
    "/get_group",
    status_code=status.HTTP_200_OK,
    response_model=List[GroupData],
)
async def get_list(
        request: Request,
):
    async with request.app.state.db.get_session() as session:
        result = list(map(lambda x:x.Group.__dict__ ,(await session.execute(
            select(Group)
        )).mappings().all()))

    return result


@router.patch(
    "/update_group/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GroupData,
)
async def update_group(
        request: Request,
        model: UpdateGroupRequest,
        id: int
):
    data = dict()

    for key, value in model.dict().items():
        if model.dict()[key] is not None:
            data[key] = value

    async with request.app.state.db.get_session() as session:
        await get_or_404(session, Group, id)
        query = sa_update(Group).where(Group.id == id).values(**data).options(joinedload(Group.users)).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()
        print(result)
        print(result.Group)

    return result


@router.delete(
    "/delete_group/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        await get_or_404(session, Group, id)
        query = sa_delete(Group).where(Group.id == id)
        await session.execute(query)
