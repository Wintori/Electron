import datetime
from sqlalchemy import insert as sa_insert, literal_column, delete as sa_delete, select, update as sa_update
from fastapi import APIRouter, status, Request
from back.app.models.item import Items
from sqlalchemy.orm import joinedload
from back.app.utils.delete import delete_from_dict
from back.app.schems import ItemRequestData, ItemResponseData
from back.app.utils.items.utils import check_in_base, get_or_404, select_all_fiels_id, update_size_by_files_id

router = APIRouter(
    prefix="",
    tags=["Дополнительные задания"],
)
