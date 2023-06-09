from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, root_validator

from ..models.order.order_model import OrderStatus, PaymentMethods, PaymentStatus
from . import product_schema, user_schema
from .cart_schema import ProductInfoInCartSchema, SizeValue


# #OrderItem
class OrderItemBaseSchema(BaseModel):
    product_id: str
    qty: int | None = Field(None, ge=1, le=99)
    size: SizeValue

    class Config:
        orm_mode = True


class OrderItemCreateSchema(OrderItemBaseSchema):  # front end doesn't have to pass order_id
    pass


class OrderItemSchema(OrderItemBaseSchema):
    order_id: str
    product_info: ProductInfoInCartSchema

    class Config:
        orm_mode = True


class OrderItemDeleteSchema(BaseModel):
    product_id: str
    order_id: str
    size: SizeValue


# Order


class OrderStatusSchema(BaseModel):
    order_status: OrderStatus = Field(
        OrderStatus.COMPLETED, description="0-> completed, 1-> canceled"
    )


class OrderBaseSchema(OrderStatusSchema):
    delivery_address: str
    discount: float = 0
    discount_code: str = ""
    total: float
    discount_total: float = 0
    shipping: float
    receiver_name: str
    payment_method: PaymentMethods = Field(PaymentMethods.credit_card)
    payment_status: PaymentStatus = Field(
        PaymentStatus.PAID, description="0 -> Pending payment, 1-> paid "
    )
    order_status: OrderStatus = Field(
        OrderStatus.COMPLETED, description="0-> completed, 1-> canceled"
    )

    class Config:
        orm_mode = True


class OrderCreateSchema(OrderBaseSchema):
    cart_id: str
    owner_id: str
    # can not be modified, so that when updating,that schema can directly inherit base schema.
    order_items: list[OrderItemCreateSchema]


base_keys = list(OrderBaseSchema.__annotations__.keys())
# all the attr in OrderBaseSchema(attr == annotations)


class OrderUpdateSchema(OrderBaseSchema):
    __annotations__ = {k: Optional[v] for k, v in OrderBaseSchema.__annotations__.items()}
    # make all the annotations in OrderBaseSchema optional and add them into this schema

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


class PaymentUrlSchema(BaseModel):
    url: HttpUrl

    class Config:
        orm_mode = True


# class OrderItemsSchema(BaseModel):
#     order_items: list[OrderItemSchema]

#     class Config:
#         orm_mode = True


class OrderSchema(OrderBaseSchema):
    id: str
    order_items: list[OrderItemSchema]
    payment_url: PaymentUrlSchema | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# orderList
class OrderInListSchema(OrderStatusSchema):
    id: str
    total: float
    discount_total: float
    created_at: datetime

    class Config:
        orm_mode = True


class ResponseOrder(BaseModel):
    list: list[OrderInListSchema]
    total: int

    class Config:
        orm_mode = True
