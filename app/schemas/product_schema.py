from datetime import datetime
from typing import Optional

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


base_keys = list(ProductBaseSchema.__annotations__.keys())
class ProductUpdateSchema(ProductBaseSchema):
    __annotations__ = {k: Optional[v] for k, v in ProductBaseSchema.__annotations__.items()}
    #must add this,or when you start to add the attr other than id,you'll get the field missing error in a row.

    id: str

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if len(values) < 2 and values.get('id'):
            raise ValueError("At least one attribute other than 'id' must be provided.")

        for attr in values:
            if attr != 'id':
                if attr not in base_keys:
                    raise ValueError(f"You've passed a non-existing attribute: {attr}")
        return values


class ProductSchema(ProductBaseSchema):
    id: str
    reviews: list[ReviewSchema] = []
    image_list: list[ProductImageUrlSchema] = []
    thumbnail_list: list[ProductImageUrlSchema] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
class FavoriteItemSchema(ProductSchema):
    pass
class FavoriteItemCreateSchema(ProductSchema):
    user_id: str
    product_id: str

