import uuid
from datetime import datetime
from enum import Enum
from typing import Dict

from decouple import config
from pydantic import BaseModel, EmailStr, Field, HttpUrl, constr, validator

from .item_schema import Item


class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: str 
    last_name: str

    class Config:
        orm_mode = True
        



class UserCreateSchema(UserBaseSchema):
    password: constr(min_length=8)
    
    
class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

class CreatePasswordSchema(BaseModel):
    password: constr(min_length=8) 

class EmailBaseSchema(BaseModel):
    email: EmailStr
class GoogleLoginSchema(EmailBaseSchema):
    pass

class UserSchema(UserBaseSchema): #used to return data
    id: str
    phone: str = ""
    verified: bool = False
    items: list[Item] = []
    upload_avatar: str = Field("", alias='avatarUpload')
    default_avatar: str = Field(config('DEFAULT_AVATAR_URL'), alias='avatarDefault')
    created_at: datetime
    updated_at: datetime
    
class UserWithTokenSchema(UserSchema):
    token: str
    refresh_token: str
class TokenSchema(BaseModel):
    token: str
class AccessAndRefreshTokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class BaseResultSchema(BaseModel):
    token: str
    refresh_token: str
    user: UserSchema
class LoginResultSchema(BaseResultSchema):
    cart_length: int
class RegisterResultSchema(BaseResultSchema):
    pass


class SupportedField(str,Enum):
    FIRSTNAME = 'first_name'
    LASTNAME = 'last_name'
    VERIFIED = 'verified'
    PHONE = 'phone'

class VerifiedValue(str,Enum):
    ZERO = "0"
    ONE = "1"

supported_fields = [field.value for field in SupportedField]
verified_values = [member.value for member in VerifiedValue]

class UserUpdateSchema(BaseModel):
    field: SupportedField = Field(description="user data's field you want to update.Only the updating to the firstname,lastName,phone and verify field is supported.")
    value: str | VerifiedValue = Field(description="data for update the field you specify.('0' -> False & '1' -> True)")

    @validator('field')
    def validate_field(cls,v):
        if v not in supported_fields:
            raise ValueError("Invalid field value, must be one of the following: {}".format(supported_fields))

    @validator('value')
    def validate_value(cls, v, values):
        field_name,field_value = values.get('field'), values.get('value')
        if field_name == 'verified' and field_value not in verified_values:
            raise ValueError("value for verified field must be '0' or '1'")
        
        return values

class UserUploadAvatarSchema(BaseModel):
    url: HttpUrl


