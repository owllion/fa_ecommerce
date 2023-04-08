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
    user_id: int
    product_id: int
    rating: float = Field(...,min = 0.5, max=5)
    comment: str
    
    class Config:
        orm_mode = True


class ReviewCreateSchema(ReviewBaseSchema):
    pass


class ReviewUpdateSchema(BaseModel):
    id: str
    rating: float | None = None
    comment: str | None = None

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if not ('rating' in values or 'comment' in values):
            raise ValueError("At least 'rating' or 'comment' must be provided.")
        return values
    

class ReviewSchema(ReviewBase):
    id: str
    created_at: datetime
    updated_at: datetime




