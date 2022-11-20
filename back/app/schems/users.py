from pydantic import BaseModel
from back.app.schems.group import GroupData


class UserData(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class UserResponse(UserData):
    pass

class CreateUserRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    group_id: int

    class Config:
        orm_mode = True

#
# class UpdateUserRequest(BaseModel):
#     full_name: str | None
#     email: str | None
#     phone: str | None
#     group_id: int | None
#
#     class Config:
#         orm_mode = True
