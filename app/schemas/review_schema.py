import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List

from decouple import config
from pydantic import BaseModel, EmailStr, Field, HttpUrl, constr, validator


class ReviewSchema(BaseModel):
    id: str
    user_id: int
    product_id: str
    rating: float = Field(...,min = 0.5, max = 5)
    comment: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

