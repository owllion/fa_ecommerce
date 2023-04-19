from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, root_validator

from . import product_schema, user_schema
from .cart_schema import ProductInfoInCartSchema, SizeValue


# #OrderItem
class OrderItemBaseSchema(BaseModel):
    product_id: int
    qty: int | None = Field(None, ge=1, le=99)
    size: SizeValue 
    class Config:
        orm_mode = True
class OrderItemCreateSchema(OrderItemBaseSchema):
    order_id: int
class OrderItemUpdateSchema(OrderItemBaseSchema):
    pass
class OrderItemSchema(OrderItemBaseSchema): 
    product: ProductInfoInCartSchema
    class Config:
        orm_mode = True

class OrderItemDeleteSchema(BaseModel):
    product_id: int
    order_id: int
    size: SizeValue 

#Order
class OrderStatus(str, Enum):
    COMPLETED = 'completed'
    CANCELED = 'canceled'

class PaymentStatus(str, Enum):
    PAID = 'paid'

class OrderBaseSchema(BaseModel):
    delivery_address: str
    discount: float = 0
    discount_code: str = ""
    total: float
    discount_total: float = 0
    shipping: float
    receiver_name: str 
    payment_method: str = "credit_card"
    payment_status: PaymentStatus = PaymentStatus.PAID
    order_status: OrderStatus = OrderStatus.COMPLETED

    class Config:
        orm_mode = True


class OrderCreateSchema(OrderBaseSchema):
    owner_id: int
    #can not be modified, so that when updating,that schema can directly inherit base schema.
    order_items: list[OrderItemSchema]


base_keys = list(OrderBaseSchema.__annotations__.keys())
class OrderUpdateSchema(OrderBaseSchema):
    __annotations__ = {k: Optional[v] for k, v in OrderBaseSchema.__annotations__.items()}
    
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


class OrderSchema(OrderBaseSchema):
    id: str
    order_items: list[OrderItemSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



