from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from .product_schema import ProductSchema


#-----
class ProductInfoForCartItemSchema(BaseModel):
    thumbnail: str
    product_name: str
    class Config:
        orm_mode = True
#----
class SizeValue(str,Enum):
    xs = 'XS'
    s = 'S'
    m = 'M'
    l = 'L'
    xl = 'XL'
class OperationType(str, Enum):
    INC = 'inc'
    DEC = 'dec'

class CartItemBaseSchema(BaseModel):
    product_id: str
    qty: int | None = Field(1, ge=1, le=99)
    size: SizeValue 
    class Config:
        orm_mode = True
class CartItemCreateSchema(CartItemBaseSchema):
    cart_id: str

#用來update cart_item table中的某個cart_item ,不是user cart裡面的     
class CartItemUpdateSchema(CartItemBaseSchema):
    pass

class CartItemSchema(CartItemBaseSchema): 
    product: ProductInfoForCartItemSchema
    class Config:
        orm_mode = True



class ItemQtySchema(BaseModel):
    qty: int | None = Field(1, ge=1,le=99)

# class AddToCartSchema(CartItemBaseSchema,ItemQtySchema):
#     pass 
class RemoveFromCartSchema(BaseModel):
    product_id: str
    size: SizeValue 
class UpdateItemQtySchema(CartItemBaseSchema):
    operation_type: OperationType


#cart 
class CartBaseSchema(BaseModel):
    user_id: str


class CartCreate(CartBaseSchema):
    pass


class CartUpdate(CartBaseSchema):
    pass


class CartSchema(CartBaseSchema):
    id: str
    cart_items: list[CartItemSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True