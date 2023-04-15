from datetime import datetime

from pydantic import BaseModel, Field

from .product_schema import ProductSchema


class CartBaseSchema(BaseModel):
    user_id: str


class CartCreate(CartBaseSchema):
    pass


class CartUpdate(CartBaseSchema):
    pass


class CartItemBaseSchema(BaseModel):
    product_id: str
    quantity: int = Field(...,ge=1,le=99)

class CartItemCreateSchema(CartItemBaseSchema):
    cart_id: str   
class CartItemUpdateSchema(CartItemBaseSchema):
    pass
class CartItemSchema(CartItemBaseSchema): 
    product = ProductSchema
    class Config:
        orm_mode = True

#cart
class CartSchema(CartBaseSchema):
    id: str
    cart_items: list[CartItemSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

   


