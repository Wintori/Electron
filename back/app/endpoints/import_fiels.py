import datetime

from dateutil import parser
from fastapi import APIRouter, status, Request, HTTPException
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update
from sqlalchemy.orm import joinedload

from back.app.logic.create_file import create_folder_os
from back.app.models.item import Items
from back.app.schems import ItemResponseData, FolderItemData
from back.app.utils.items.utils import check_in_base, get_or_404, select_all_fiels_id
from back.config.file_save_config import DEFOULT_PATH

router = APIRouter(
    prefix="",
    tags=["Some tag"],
)


@router.post(
    "/create_folder",
    status_code=status.HTTP_201_CREATED,
)
async def create_folder(
        request: Request,
        model: FolderItemData,
):
    async with request.app.state.db.get_session() as session:
        in_base, res = await check_in_base(session, Items, model.id)
        if res:
            HTTPException(status_code=status.HTTP_409_CONFLICT,
                          detail=f"Conflict, file with id = {model.id} already in base")

        if model.parent_id:
            # Проверка что мы не пытаемся добавить к несуществующему родителю
            parent = await get_or_404(session, Items, model.parent_id)

        # todo Создать возхмодность переносить папки вместе с файлами
        # if in_base:
        #     data = model.dict()
        #     del data["id"]
        #
        #     query = sa_update(Items). \
        #         where(Items.id == model.id). \
        #         values(**data, url=creation_url). \
        #         returning(literal_column("*"))
        # else:
        if parent:
            creation_url = parent.url + model.name + "/"
        else:
            creation_url = DEFOULT_PATH + model.name + "/"
        query = sa_insert(Items). \
            values(**model.dict(), url=creation_url, date=datetime.datetime.now()). \
            returning(literal_column("*"))
        create_folder_os(creation_url)
        await session.execute(query)

        await session.commit()


#
# @router.post(
#     "/import_folders",
#     status_code=status.HTTP_201_CREATED,
# )
# async def create(
#         request: Request,
#         model: ItemRequestData,
# ):
#     """
#
#     Загрузка структуры папок
#     :param request:
#     :param model:
#     :return:
#     """
#     async with request.app.state.db.get_session() as session:
#         files_data = set()
#         for item in model.items:
#             in_base, res = await check_in_base(session, Items, item.id)
#             if item.parent_id:
#                 # Проверка что мы не пытаемся добавить к несуществующему родителю
#                 await get_or_404(session, Items, item.parent_id)
#
#             if in_base:
#                 data = item.dict()
#                 del data["id"]
#                 data["date"] = model.updateDate.replace(tzinfo=None)
#                 query = sa_update(Items). \
#                     where(Items.id == item.id). \
#                     values(**data). \
#                     returning(literal_column("*"))
#
#             else:
#                 item.date = model.updateDate.replace(tzinfo=None)
#                 query = sa_insert(Items). \
#                     values(**item.dict()). \
#                     returning(literal_column("*"))
#
#             old_size = 0  # Необходим для того что бы при обновлении размера файла
#             if item.type == "FILE":
#                 if in_base:
#                     old_size = res.size
#
#                 files_data.add((item.id, old_size))
#
#             await session.execute(query)
#
#         await update_size_by_files_id(session, files_data)
#
#         await session.commit()


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(request: Request, item_id: str, date: datetime.datetime):
    query = sa_delete(Items).where(Items.id == item_id)

    async with request.app.state.db.get_session() as session:
        res = await get_or_404(session, Items, item_id)
        minus_size = res.size
        res = res.parent_id

        # delete_from_dict(request.app.tree, item_id)
        while res:
            update_parent = sa_update(Items). \
                where(Items.id == res). \
                values(date=date.replace(tzinfo=None), size=Items.size - minus_size). \
                returning(literal_column("parent_id"))

            res = (await session.execute(update_parent)).scalars().first()
            print(res)
        await session.execute(query)
        await session.commit()


@router.get('/get_files', status_code=status.HTTP_200_OK)
async def get_files(request: Request):
    async with request.app.state.db.get_session() as session:
        files_id = await select_all_fiels_id(session)
        return files_id


@router.get('/nodes/{id}', response_model=ItemResponseData, status_code=status.HTTP_200_OK)
async def get_files(id: str, request: Request):
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
            temp = res.scalars().first()
            print(temp)
            for i in temp.children:
                stack.append(i)
            # print(f"{stack=}")
            # print("%"*150)
    # print("hahaha")
    return root


@router.get('/updates', response_model=ItemResponseData, status_code=200)
async def updates(date: str, request: Request):
    async with request.app.state.db.get_session() as session:
        query = select(Items).where(Items.date <= parser.parse(date),
                                    Items.date >= parser.parse(date) - datetime.timedelta(
                                        hours=24))
        res = await session.execute(query)
        res = res.scalars().all()
    return res
