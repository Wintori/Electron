from typing import List

from pydantic import BaseModel


class GroupData(BaseModel):
    id: int
    name: str
    description: str


class GroupResponse(GroupData):
    from back.app.schems.users import UserData
    users: List[UserData]

    class Config:
        orm_mode = True


class CreateGroupRequest(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True
#
#
# class UpdateGroupRequest(BaseModel):
#     name: str | None
#     description: str | None
#
#     class Config:
#         orm_mode = True
