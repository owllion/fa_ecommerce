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

from . import cart_schema
from .review_schema import ReviewSchema


# for image url
class ProductImageUrlSchema(BaseModel):
    url: HttpUrl

    class Config:
        orm_mode = True


class ProductBaseSchema(BaseModel):
    product_name: str = Field(..., max_length=50)
    description: str = Field(None, max_length=800)
    thumbnail: str
    price: float = Field(..., ge=0.0)
    brand: str = Field(..., max_length=30)
    category: str = Field(..., max_length=30)
    color: str = Field(..., max_length=20)

    class Config:
        orm_mode = True


class ProductCreateSchema(ProductBaseSchema):
    pass


base_keys = list(ProductBaseSchema.__annotations__.keys())


class ProductUpdateSchema(ProductBaseSchema):
    __annotations__ = {k: Optional[v] for k, v in ProductBaseSchema.__annotations__.items()}
    # must add this,or when you start to add the attr other than id,you'll get the field missing error in a row.
    # coz this means all the attrs inside the ProductBaseSchema would be optional.

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


class SerializedProductSchema(ProductBaseSchema):
    created_at: datetime
    updated_at: datetime


class ProductSchema(ProductBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        # 自動去populate而不是原本的lazy loading
        # 也可讓pydantic model去讀取db model


# for detail page
class SingleProductSchema(ProductSchema):
    reviews: list[ReviewSchema] = []
    images: list[ProductImageUrlSchema]
    thumbnails: list[ProductImageUrlSchema]

    class Config:
        orm_mode = True


# for query product list
class PaginateProductsSchema(BaseModel):
    page: int = 1
    limit: int = 12
    keyword: str = ""
    price: str = ""
    brands: list[str] | str = ""
    categories: list[str] | str = ""
    sort_by: str = ""
    order_by: str = ""

    class Config:
        orm_mode = True


class ResponsePaginateProductsSchema(BaseModel):
    list: list[ProductSchema]
    total: int

    class Config:
        orm_mode = True


class FavoriteItemSchema(cart_schema.ProductInfoInCartSchema):
    pass


class FavoriteItemCreateSchema(ProductSchema):
    user_id: str
    product_id: str


class ToggleFavoriteSchema(BaseModel):
    product_id: str
