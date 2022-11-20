from pydantic import BaseModel


class APIKeyResponse(BaseModel):
    id: int
    name: str
    type: str
    auth_string: str

    class Config:
        orm_mode = True


class CreateAPIKeyRequest(BaseModel):
    name: str
    type: str
    auth_string: str

    class Config:
        orm_mode = True

#
# class UpdateAPIKeyRequest(BaseModel):
#     name: str | None
#     type: str | None
#     auth_string: str | None
#
#     class Config:
#         orm_mode = True
