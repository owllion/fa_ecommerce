from pydantic import BaseModel
from .item import Item
from decouple import config

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

# class User(UserBase):
#     id: int
#     email: bool
#     username: str 
#     item: list[Item] = []
#     phone: str = ""
#     avatarUpload: str = ""
#     avatarDefault: config('DEFAULT_AVATAR_URL')
#     class Config:
#         orm_mode = True