from pydantic import BaseModel,Field, EmailStr

from decouple import config
from .item import Item

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=5, description="Should be longer than 5")
class User(UserBase):
    id: str
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