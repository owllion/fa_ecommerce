from datetime import datetime
from typing import List

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    constr,
    root_validator,
    validator,
)

from .review_schema import ReviewSchema


class ProductImageUrlSchema(BaseModel):
    url: str
    product_id: str
class ProductBaseSchema(BaseModel):
    product_name: str = Field(...,max_length=50)
    thumbnail: str
    price: float = Field(..., ge=0.0)
    brand: str = Field(...,max_length=30)
    category: str = Field(...,max_length=30)
    size: str = Field("F")
    color: str = Field(...,max_length=20)
    description: str = Field(None, max_length=800)
    stock: int = Field(..., ge=0)
    availability: bool 
    sales: int = Field(..., ge=0)
    class Config:
        orm_mode = True


class ProductCreateSchema(ProductBaseSchema):
    pass
    
class ProductUpdateSchema(BaseModel):
    id: str
    product_name: str | None = Field(None, max_length=50)
    thumbnail: str | None = None
    price: float | None = Field(None, ge=0.0)
    brand: str | None = Field(None, max_length=30)
    category: str | None = Field(None, max_length=30)
    size: str | None = None
    color: str | None = Field(None, max_length=20)
    description: str | None = Field(None, max_length=800)
    stock: int | None = Field(None, ge=0)
    availability: bool | None = None
    sales: int | None = Field(None, ge=0)

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if not any(attr for attr in values.values() if attr != 'id'):
            raise ValueError("At least one attribute other than 'id' must be provided.")
        return values
class ProductSchema(ProductBaseSchema):
    id: str
    reviews: List[ReviewSchema]
    image_list: List[ProductImageUrlSchema]
    thumbnail_list: List[ProductImageUrlSchema]
    created_at: datetime
    updated_at: datetime
class LikeProductSchema(ProductSchema):
    pass
class LikeProductCreateSchema(ProductSchema):
    user_id: str
    product_id: str

