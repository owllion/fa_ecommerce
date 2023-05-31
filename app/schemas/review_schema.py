import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

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


class ReviewBaseSchema(BaseModel):
    rating: float = Field(..., ge=0.5, le=5)
    comment: str


class ReviewCreateSchema(ReviewBaseSchema):
    user_id: str
    product_id: str


base_keys = list(ReviewBaseSchema.__annotations__.keys())


class ReviewUpdateSchema(BaseModel):
    __annotations__ = {k: Optional[v] for k, v in ReviewBaseSchema.__annotations__.items()}

    id: str

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if len(values) < 2 and values.get("id"):
            raise ValueError("At least one attribute other than 'id' must be provided.")

        for attr in values:
            if attr != "id":
                if attr not in base_keys:
                    raise ValueError(f"You've passed a non-existing attribute: {attr}")
        return values


class ReviewUserSchema(BaseModel):
    first_name: str
    last_name: str
    default_avatar: str
    upload_avatar: str

    class Config:
        orm_mode = True


class ReviewSchema(ReviewBaseSchema):
    id: str
    user: ReviewUserSchema
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RelatedProductSchema(BaseModel):
    id: str
    thumbnail: str
    product_name: str

    class Config:
        orm_mode = True


class UserReviewListSchema(ReviewSchema):
    product: RelatedProductSchema

    class Config:
        orm_mode = True
