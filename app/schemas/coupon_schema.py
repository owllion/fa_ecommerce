from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Partial, root_validator


class CouponBase(BaseModel):
    code: str
    description: str = ""
    amount: Decimal
    expiry_date: datetime
    minimum_amount: Decimal
    discount_type: str


class CouponCreate(CouponBase):
    user_id: int

class CouponUpdate(BaseModel):
    id: str
    code: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    expiry_date: datetime | None = None
    minimum_amount: Decimal | None = None
    discount_type: str | None = None

    @root_validator(pre=True)
    def check_at_least_one_attribute(cls, values):
        if not any(attr for attr in values.values() if attr != 'id'):
            raise ValueError("At least one attribute other than 'id' must be provided.")
        return values

class Coupon(CouponBase):
    id: str
    user_id: int
    is_used: bool


    class Config:
        orm_mode = True