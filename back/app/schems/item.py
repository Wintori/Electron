from datetime import datetime
from enum import Enum
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator, root_validator


class SystemItemType(str, Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class SystemItemTag(str, Enum):
    Document = "Document"
    Template = "Template"
    Report = "Report"
    Export = "Export"
    Other = "Other"


# class InternalItemData(BaseModel):
#     id: str
#     url: str | None = None
#     date: datetime | None
#     parent_id: str | None
#     type: SystemItemType
#     size: int | None = 0
#
#     class Config:
#         orm_mode = True


# class ItemData(BaseModel):
#     id: int
#     date: datetime
#     parent_id: int | None
#     size: int
#     url: str
#     name: str
#     tag: SystemItemTag
#     type: SystemItemType
#
#     class Config:
#         orm_mode = True
#
#
# class FolderItemRequest(BaseModel):
#     parent_id: int | None = None
#     name: str
#
#     class Config:
#         orm_mode = True
#
#
# class FileItemRequest(BaseModel):
#     id: int | None = None
#     parent_id: int | None
#
#     class Config:
#         orm_mode = True
#
#
# class ItemTagResponseData(BaseModel):
#     items: List[ItemData]
#
#
# class ItemResponseData(ItemData):
#     children: List | None = []
#
#     @validator("children")
#     def replace_empty(cls, val):
#         return val or None
#
#     def get_child(self, index):
#         if len(self.children) > index:
#             return self.children[index]
#         return None
#
#
# class Error(BaseModel):
#     code: int
#     message: str
#
#     class Config:
#         orm_mode = True
