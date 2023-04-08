import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List

from decouple import config
from pydantic import BaseModel, EmailStr, Field, HttpUrl, constr, validator

from .review_schema import ReviewSchema


class ProductImageUrlSchema(BaseModel):
    url: str
    product_id: str

class ProductSchema(BaseModel):
    id: str
    product_name: str
    thumbnail: str
    price: float
    brand: str
    category: str
    color: str 
    size: str = 'F'
    description: str = ''
    stock: int
    availability: bool
    sales: int
    qty: int
    is_checked: bool = False
    image_list: List[ProductImageUrlSchema]
    thumbnail_list: List[ProductImageUrlSchema]
    reviews: List[ReviewSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

