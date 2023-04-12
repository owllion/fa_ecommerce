from datetime import datetime

from pydantic import BaseModel

from . import user_schema
from .review_schema import ReviewSchema


class UserReviewBaseSchema(BaseModel):
    user_id: int
    product_id: int
    rating: float
    comment: str

class UserReviewCreateSchema(UserReviewBaseSchema):
    pass

class UserReviewSchema(UserReviewBaseSchema):
    id: str
    user: user_schema.UserSchema
    review: ReviewSchema
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
