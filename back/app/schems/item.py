from datetime import datetime
from enum import Enum
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator, root_validator


class SystemItemType(str, Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class InternalItemData(BaseModel):
    id: str
    url: str | None = None
    date: datetime | None
    parent_id: str | None
    type: SystemItemType
    size: int | None = 0

    class Config:
        orm_mode = True


class ItemData(BaseModel):
    id: str
    url: str | None = None
    parent_id: str | None = None

    type: SystemItemType
    date: datetime | None
    size: int | None = 0

    @root_validator
    def checker(cls, v):
        if v.get('type').value == "FILE" and (v.get('size') <= 0 or len(v.get('url')) > 255):
            raise HTTPException(400, detail="Validation Failed")
        return v


class FolderItemData(BaseModel):
    id: int
    # url: str | None = None
    parent_id: int | None = None
    name: str
    type: SystemItemType = SystemItemType.FOLDER
    # date: datetime | None
    # size: int | None = 0

    class Config:
        orm_mode = True





class ItemResponseData(InternalItemData):
    children: List | None = []

    @validator("children")
    def replace_empty(cls, val):
        return val or None

    def get_child(self, index):
        if len(self.children) > index:
            return self.children[index]
        return None


class ItemRequestData(BaseModel):
    items: List[ItemData]
    updateDate: datetime

    class Config:
        orm_mode = True


class Error(BaseModel):
    code: int
    message: str

    class Config:
        orm_mode = True
