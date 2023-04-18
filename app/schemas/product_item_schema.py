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
class ProductItemCreateSchema(ProductItemBaseSchema,ProductIdSchema):
    pass

base_keys = list(ProductItemBaseSchema.__annotations__.keys())

class ProductItemUpdateSchema(ProductItemBaseSchema,ProductIdSchema):
    __annotations__ = {k: Optional[v] for k, v in ProductItemBaseSchema.__annotations__.items()}

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if len(values) < 2 and values.get('product_id'):
            raise ValueError("At least one attribute other than 'product_id' must be provided.")

        for attr in values:
            if attr != 'product_id':
                if attr not in base_keys:
                    raise ValueError(f"You've passed a non-existing attribute: {attr}")
        return values
    
class ProductItemDeleteSchema(ProductIdSchema):
    size_id: str

class ProductItemSchema(ProductItemBaseSchema,ProductIdSchema):
    class Config:
            orm_mode = True