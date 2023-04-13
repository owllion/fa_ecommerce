from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, root_validator


class CouponBaseSchema(BaseModel):
    code: str
    description: str = ""
    amount: Decimal
    expiry_date: datetime
    minimum_amount: Decimal
    discount_type: str

class CouponCreateSchema(CouponBaseSchema):
    user_id: int


base_keys = list(CouponBaseSchema.__annotations__.keys())

class CouponUpdateSchema(BaseModel):
    __annotations__ = {k: Optional[v] for k, v in CouponBaseSchema.__annotations__.items()}

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

class CouponSchema(CouponBaseSchema):
    id: str
    user_id: int
    is_used: bool

    class Config:
        orm_mode = True

class AppliedCouponResultSchema(BaseModel):
    final_price_after_discount: Decimal
    discountedAmount: Decimal