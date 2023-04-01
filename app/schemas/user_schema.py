from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr, constr,Field
from enum import Enum

from decouple import config
from .item_schema import Item

class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str 

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: constr(min_length=8)
    
    
class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8) 
    
class GoogleLoginSchema(BaseModel):
    email: EmailStr


class UserSchema(UserBaseSchema): #used to return data
    id: str
    verified: bool = False
    items: list[Item] = []
    upload_avatar: str = ""
    default_avatar: str = config('DEFAULT_AVATAR_URL')
    created_at: datetime
    updated_at: datetime

class UserWithTokenSchema(UserSchema):
    access_token: str
    refresh_token: str

class SupportedFiled(str,Enum):
    USERNAME = 'username'
    VERIFIED = 'verified'

class VerifiedValue(str,Enum):
    ZERO = "0"
    ONE = "1"
class UserUpdateSchema(BaseModel):
    id: str
    field: SupportedFiled = Field(description="user data's field you want to update.Only the updating to the username and verify field is supported.")
    value: str | VerifiedValue = Field(description="data for update the field you specify.('0' -> False & '1' -> True)")
