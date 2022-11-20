from datetime import datetime
from enum import Enum
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator, root_validator


class DataSourcesStatus(str, Enum):
    Connected = "Connected"
    Starting = "Starting"
    Stopped = "Stopped"
    Error = "Error"


class DataSourcesResponse(BaseModel):
    id: int
    name: str
    type: str
    status: DataSourcesStatus
    date: datetime

    class Config:
        orm_mode = True


class CreateDataSourcesRequest(BaseModel):
    name: str
    type: str
    status: DataSourcesStatus

    class Config:
        orm_mode = True


# class UpdateDataSourcesRequest(BaseModel):
#     name: str | None
#     type: str | None
#     status: DataSourcesStatus | None
#     date: datetime | None
#
#     class Config:
#         orm_mode = True
