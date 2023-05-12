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


class ProductIdSchema(BaseModel):
    product_id: str


class ProductItemBaseSchema(BaseModel):
    size_id: str
    stock: int = Field(..., ge=1)
    sales: int

    class Config:
        orm_mode = True


class ProductItemCreateSchema(ProductItemBaseSchema, ProductIdSchema):
    pass


base_keys = list(ProductItemBaseSchema.__annotations__.keys())


class ProductItemUpdateSchema(ProductItemBaseSchema, ProductIdSchema):
    __annotations__ = {k: Optional[v] for k, v in ProductItemBaseSchema.__annotations__.items()}
    # 沒有Field的能才用這，其餘有需要額外驗證的(如下)還是只能自己寫

    stock: int | None = Field(None, ge=1)
    sales: int | None = Field(None, ge=1)

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if len(values) < 2 and values.get("product_id"):
            raise ValueError("At least one attribute other than 'product_id' must be provided.")

        for attr in values:
            if attr != "product_id":
                if attr not in base_keys:
                    raise ValueError(f"You've passed a non-existing attribute: {attr}")
        return values


class ProductItemDeleteSchema(ProductIdSchema):
    size_id: str


class SizeSchema(BaseModel):
    value: str

    class Config:
        orm_mode = True


class ProductItemSchema(ProductItemBaseSchema, ProductIdSchema):
    size: SizeSchema

    class Config:
        orm_mode = True


# for best_seller product
class BestSellerProductSchema(BaseModel):
    thumbnail: HttpUrl
    product_name: str
    price: float
    id: str

    class Config:
        orm_mode = True


class ProductItemWithProductSchema(BaseModel):
    parent_product: BestSellerProductSchema

    class Config:
        orm_mode = True
