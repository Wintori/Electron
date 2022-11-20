from typing import Optional, List

from fastapi import APIRouter, status, Request
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update

from back.app.models.api_keys import APIKeys

from back.app.schems.api_keys import CreateAPIKeyRequest, APIKeyResponse, UpdateAPIKeyRequest
from back.app.utils.items.utils import get_or_404

router = APIRouter(
    prefix="/api_keys",
    tags=["API keys CRUD + List"],
)


@router.post(
    "/create_api_keys",
    status_code=status.HTTP_201_CREATED,
    response_model=APIKeyResponse,
)
async def create(
        request: Request,
        model: CreateAPIKeyRequest,

):
    async with request.app.state.db.get_session() as session:
        query = sa_insert(APIKeys).values(**model.dict()).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()
        await session.commit()

    return result


@router.get(
    "/get_api_keys/{id}",
    status_code=status.HTTP_200_OK,
    response_model=APIKeyResponse,
)
async def get_data(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        result = await get_or_404(session, APIKeys, id)
    return result


@router.get(
    "/get_api_keys",
    status_code=status.HTTP_200_OK,
    response_model=List[APIKeyResponse],
)
async def get_list(
        request: Request,
):
    async with request.app.state.db.get_session() as session:
        result = (await session.execute(
            select(APIKeys)
        )).scalars().all()
    return result


@router.patch(
    "/update_api_keys/{id}",
    status_code=status.HTTP_200_OK,
    response_model=APIKeyResponse,
)
async def update_api_keys(
        request: Request,
        model: UpdateAPIKeyRequest,
        id: int
):
    data = dict()

    for key, value in model.dict().items():
        if model.dict()[key] is not None:
            data[key] = value

    async with request.app.state.db.get_session() as session:
        await get_or_404(session, APIKeys, id)
        query = sa_update(APIKeys).where(APIKeys.id == id).values(**data).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()

    return result


@router.delete(
    "/delete_api_keys/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_api_keys(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        await get_or_404(session, APIKeys, id)
        query = sa_delete(APIKeys).where(APIKeys.id == id)
        await session.execute(query)
