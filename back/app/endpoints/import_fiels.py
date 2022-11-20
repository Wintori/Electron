import datetime
from typing import Optional

from dateutil import parser
from fastapi import APIRouter, status, Request, HTTPException, File, UploadFile
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update
from sqlalchemy.orm import joinedload
from starlette.responses import FileResponse

from back.app.logic.create_file import create_folder_os, delete_folder_os, check_file_in_folder, save_file_to_uploads, \
    get_file_size
from back.app.models.item import Items
from back.app.schems import ItemResponseData, FolderItemRequest, SystemItemType, SystemItemTag, ItemData, \
    ItemTagResponseData
from back.app.utils.items.utils import check_in_base, get_or_404, select_all_fiels_id, select_all_items_id_by_tag
from back.config.file_save_config import DEFOULT_PATH

router = APIRouter(
    prefix="/fif",
    tags=["Work with files and folders"],
)


@router.post(
    "/create_folder",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemData,
)
async def create_folder(
        request: Request,
        model: FolderItemRequest,
        tag: SystemItemTag = SystemItemTag.Other,

):
    async with request.app.state.db.get_session() as session:
        parent = None
        if model.parent_id:
            # Проверка что мы не пытаемся добавить к несуществующему родителю
            parent = await get_or_404(session, Items, model.parent_id)

            if parent.type == SystemItemType.FILE:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict parent is file ")
            if parent.tag != tag:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Conflict, folder {parent.url} save only {parent.tag}")

        if parent is not None:
            creation_url = parent.url + model.name + "/"
        else:
            creation_url = DEFOULT_PATH + model.name + "/"

        if check_file_in_folder(creation_url):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Conflict, file with name = {model.name} already created ")

        query = sa_insert(Items). \
            values(**model.dict(), url=creation_url, type=SystemItemType.FOLDER, tag=tag). \
            returning(literal_column("*"))
        result = (await session.execute(query)).mappings().first()

        await session.commit()
        create_folder_os(creation_url)

    return result


@router.post(
    "/create_file",
    status_code=status.HTTP_201_CREATED,
    # response_model=ItemData,
)
async def create_file(
        request: Request,
        parent_id: Optional[int] = None,
        tag: SystemItemTag = SystemItemTag.Other,
        file: UploadFile = File(...),
):
    name = file.filename
    async with request.app.state.db.get_session() as session:
        parent = None
        if parent_id:
            # Проверка что мы не пытаемся добавить к несуществующему родителю
            parent = await get_or_404(session, Items, parent_id)
            if parent is not None:
                if parent.tag != tag:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail=f"Conflict, folder {parent.url} save only {parent.tag}")
        # todo Создать возхмодность переносить папки вместе с файлами

        creation_url = parent.url if parent else DEFOULT_PATH

        if check_file_in_folder(creation_url + name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Conflict, file with name = {name} already in folder")

        await save_file_to_uploads(creation_url, file, name)
        size = get_file_size(creation_url + name)

        if parent_id is None:
            query = sa_insert(Items). \
                values(url=creation_url + name, type=SystemItemType.FILE, tag=tag, size=size). \
                returning(literal_column("*"))
        else:
            query = sa_insert(Items). \
                values(parent_id=parent_id, url=creation_url + name, type=SystemItemType.FILE, tag=tag, size=size). \
                returning(literal_column("*"))

        result = (await session.execute(query)).mappings().first()
        res = result.parent_id
        # Обновляем размер папок
        while res is not None:
            update_parent = sa_update(Items). \
                where(Items.id == res). \
                values(date=datetime.datetime.now(), size=Items.size + size). \
                returning(literal_column("parent_id"))

            res = (await session.execute(update_parent)).mappings().first().parent_id
        await session.commit()
        return result


@router.post(
    "/create_file_by_path",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemData,
)
async def create_file_by_path(
        request: Request,
        tag: SystemItemTag = SystemItemTag.Other,
        file_url: str = DEFOULT_PATH,
        file: UploadFile = File(...),
):
    name = file.filename
    async with request.app.state.db.get_session() as session:
        # Проверка что мы не пытаемся добавить к несуществующему родителю
        # print(file_url)
        # if check_file_in_folder(file_url):
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        #                         detail=f"No such path {file_url}")

        que = select(Items).where((Items.url == file_url))
        par = (await session.execute(que)).mappings().first()
        print(par.Items)
        if par is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Conflict with state on server {file_url}")

        else:
            if par.Items.tag != tag:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Conflict, folder {par.Items.url} save only {par.Items.tag}")
        # todo Создать возхмодность переносить папки вместе с файлами
        if check_file_in_folder(file_url + name):
            return HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail=f"Conflict, file with name = {name} already in folder")
        else:
            query = sa_insert(Items). \
                values(parent_id=par.Items.id, url=file_url, type=SystemItemType.FILE, tag=tag). \
                returning(literal_column("*"))

        result = (await session.execute(query)).mappings().first()
        await save_file_to_uploads(file_url, file, name)
        await session.commit()
        return result


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        request: Request,
        item_id: int
):
    query = sa_delete(Items).where(Items.id == item_id)

    async with request.app.state.db.get_session() as session:
        res = await get_or_404(session, Items, item_id)
        minus_size = res.size
        url = res.url
        type = res.type
        res = res.parent_id
        while res is not None:
            update_parent = sa_update(Items). \
                where(Items.id == res). \
                values(date=datetime.datetime.now(), size=Items.size - minus_size). \
                returning(literal_column("parent_id"))

            res = (await session.execute(update_parent)).mappings().first().parent_id
        await session.execute(query)
        await session.commit()
    delete_folder_os(url, type == SystemItemType.FOLDER)


@router.delete(
    '/delete_by_url',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_by_url(
        request: Request,
        url: str,
        date: datetime.datetime
):
    query = sa_delete(Items).where(Items.url == url)

    async with request.app.state.db.get_session() as session:
        res = await session.execute(select(Items).where(Items.url == url)).mappings().first()
        minus_size = res.size
        res = res.parent_id

        while res:
            update_parent = sa_update(Items). \
                where(Items.id == res). \
                values(date=date.replace(tzinfo=None), size=Items.size - minus_size). \
                returning(literal_column("parent_id"))

            res = (await session.execute(update_parent)).mappings().first()
        await session.execute(query)
        await session.commit()
    delete_folder_os(res.url, res.type == SystemItemType.FOLDER)


@router.get(
    '/get_by_tag',
    status_code=status.HTTP_200_OK,
    # response_model=ItemTagResponseData,
)
async def get_files_by_tag(
        request: Request,
        tag: SystemItemTag = SystemItemTag.Other,
):
    async with request.app.state.db.get_session() as session:
        files = await select_all_items_id_by_tag(session, tag)
        return {"items": files}


@router.get(
    '/get_by_tag_and_path',
    status_code=status.HTTP_200_OK,
    # response_model=ItemTagResponseData,
)
async def get_files_by_tag(
        request: Request,
        tag: SystemItemTag = SystemItemTag.Other,
        file_url: str = DEFOULT_PATH,
):
    async with request.app.state.db.get_session() as session:
        query = select(Items).where(
            (Items.tag == tag) & (Items.url == file_url) & (Items.type == SystemItemType.FOLDER))
        parent = (await session.execute(query)).scalars().first()
        if parent is None:
            return []
        files_query = select(Items).where(Items.parent_id == parent.id)
        files = (await session.execute(files_query)).scalars().all()
        # print(type(files))
        # print(ItemTagResponseData(files))
        return {"items": files}


@router.get(
    '/nodes/{id}',
    response_model=ItemResponseData,
    status_code=status.HTTP_200_OK
)
async def get_files(
        id: int,
        request: Request
):
    async with request.app.state.db.get_session() as session:
        query = select(Items).where(Items.id == id).options(joinedload(Items.children))
        res = await session.execute(query)
        root = res.scalars().first()
        stack = [*root.children]

        while stack:
            cur = stack.pop()
            if not cur:
                continue
            query = select(Items).where(Items.id == cur.id).options(joinedload(Items.children))
            res = await session.execute(query)
            temp = res.mappings().first()
            print(temp)
            for i in temp.Items.children:
                stack.append(i)

    return root


@router.get("/api/download", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def download_file(
        request: Request,
        file_id: int,
        media_type: str,
        # db: Session = Depends(get_db)
):
    # todo сделатть преевод файлов в разные форматы
    async with request.app.state.db.get_session() as session:
        res = await get_or_404(session, Items, file_id)
    file_resp = FileResponse(res.url,
                             media_type=media_type,
                             filename=res.name)
    return file_resp
    # response.status_code = status.HTTP_200_OK
    # return file_resp
    # else:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'msg': 'File not found'}
# @router.get('/updates', response_model=ItemResponseData, status_code=200)
# async def updates(date: str, request: Request):
#     async with request.app.state.db.get_session() as session:
#         query = select(Items).where(Items.date <= parser.parse(date),
#                                     Items.date >= parser.parse(date) - datetime.timedelta(
#                                         hours=24))
#         res = await session.execute(query)
#         res = res.mappings().all()
#     return res
