from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, root_validator

from . import product_schema, user_schema


#OrderItem
class OrderItemBaseSchema(BaseModel):
    order_id: int
    product_id: int

    class Config:
        orm_mode = True

class OrderItemCreateSchema(OrderItemBaseSchema):
    pass

class OrderItemSchema(OrderItemBaseSchema):
    id: str
    product: product_schema.ProductSchema
    updated_at: datetime
    created_at: datetime


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


class OrderUpdateSchema(OrderBaseSchema):
    id: str
    
    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if not any(attr for attr in values.values() if attr != 'id'):
            raise ValueError("At least one attribute other than 'id' must be provided.")
        return values


class OrderSchema(OrderBaseSchema):
    id: str
    owner_id: int
    order_items: List[OrderItemSchema]
    created_at: datetime
    updated_at: datetime



