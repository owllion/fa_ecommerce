from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr, constr


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