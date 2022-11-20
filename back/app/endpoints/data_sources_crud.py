from typing import Optional, List

from fastapi import APIRouter, status, Request, HTTPException, File, UploadFile
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update

from back.app.models.data_sources import DataSources

from back.app.schems.data_sources import CreateDataSourcesRequest, DataSourcesResponse, UpdateDataSourcesRequest
from back.app.utils.items.utils import check_in_base, get_or_404, select_all_fiels_id, select_all_items_id_by_tag

router = APIRouter(
    prefix="/ds",
    tags=["Data sources CRUD + List"],
)


@router.post(
    "/create_data_source",
    status_code=status.HTTP_201_CREATED,
    response_model=DataSourcesResponse,
)
async def create(
        request: Request,
        model: CreateDataSourcesRequest,

):
    async with request.app.state.db.get_session() as session:
        query = sa_insert(DataSources).values(**model.dict()).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()
        await session.commit()

    return result


@router.get(
    "/get_data_source/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DataSourcesResponse,
)
async def get_data(
        request: Request,
        id: int

):
    async with request.app.state.db.get_session() as session:
        result = await get_or_404(session, DataSources, id)
    return result


@router.get(
    "/get_data_source",
    status_code=status.HTTP_200_OK,
    response_model=List[DataSourcesResponse],
)
async def get_list(
        request: Request,
):
    async with request.app.state.db.get_session() as session:
        result = (await session.execute(
            select(DataSources)
        )).scalars().all()
    return result


@router.patch(
    "/update_data_source/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DataSourcesResponse,
)
async def update_data_sources(
        request: Request,
        model: UpdateDataSourcesRequest,
        id: int
):
    data = dict()

    for key, value in model.dict().items():
        if model.dict()[key] is not None:
            data[key] = value

    async with request.app.state.db.get_session() as session:
        await get_or_404(session, DataSources, id)
        query = sa_update(DataSources).where(DataSources.id == id).values(**data).returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()

    return result


@router.delete(
    "/delete_data_source/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_data_sources(
        request: Request,
        id: int
):
    async with request.app.state.db.get_session() as session:
        await get_or_404(session, DataSources, id)
        query = sa_delete(DataSources).where(DataSources.id == id)
        await session.execute(query)
