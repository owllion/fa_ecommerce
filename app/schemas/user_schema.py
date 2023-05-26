from datetime import datetime
from enum import Enum
from typing import Optional

from decouple import config
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    constr,
    root_validator,
    validator,
)


class LoginTypeValue(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    GITHUB = "github"
    FACEBOOK = "facebook"


class EmailBaseSchema(BaseModel):
    email: EmailStr


class UserBaseSchema(EmailBaseSchema, BaseModel):
    first_name: str
    last_name: str
    verified: bool = False

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: constr(min_length=8) | None = None
    # google login doesn't need the pwd

    upload_avatar: HttpUrl | None = None
    # google&github login will have avatar


class LoginUserSchema(EmailBaseSchema, BaseModel):
    password: str


class LoginTypeCreateSchema(BaseModel):
    value: LoginTypeValue | None = Field(LoginTypeValue.EMAIL)


class LoginTypeSchema(BaseModel):
    value: str

    class Config:
        orm_mode = True


class ModifyPasswordSchema(BaseModel):
    password: constr(min_length=8)


class ResetPasswordSchema(ModifyPasswordSchema):
    token: str


class UserSchema(UserBaseSchema):
    id: str
    phone: str = ""
    upload_avatar: str = ""
    default_avatar: str = Field(config("DEFAULT_AVATAR_URL"))
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TokenBaseSchema(BaseModel):
    token: str
    refresh_token: str


class UserWithTokenSchema(UserSchema, TokenBaseSchema):
    pass
    # complete user data with token


class TokenSchema(BaseModel):
    token: str
    # for verification


class AccessAndRefreshTokenSchema(TokenBaseSchema):
    pass
    # only return token pair


class BaseResultSchema(TokenBaseSchema):
    user: UserSchema


class LoginResultSchema(BaseResultSchema):
    cart_length: int


class RegisterResultSchema(BaseResultSchema):
    pass


class SupportedField(str, Enum):
    FIRSTNAME = "first_name"
    LASTNAME = "last_name"
    VERIFIED = "verified"
    PHONE = "phone"


class VerifiedValue(str, Enum):
    ZERO = "0"
    ONE = "1"


base_keys = list(UserBaseSchema.__annotations__.keys())


class UserUpdateSchema(BaseModel):
    __annotations__ = {k: Optional[v] for k, v in UserBaseSchema.__annotations__.items()}

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if len(values) < 1:
            raise ValueError("Please pass at least one attribute.")

        for attr in values:
            if attr not in base_keys:
                raise ValueError(f"You've passed a non-existing attribute: {attr}")
        return values


class UserUploadAvatarSchema(BaseModel):
    url: HttpUrl
