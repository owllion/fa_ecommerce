from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, root_validator


class DiscountType(str, Enum):
    fixed_amount = "fixed_amount"
    percentage = "percentage"


class CouponBaseSchema(BaseModel):
    code: str
    description: str = ""
    discount_type: DiscountType
    amount: float
    minimum_amount: float
    expiry_date: datetime
    class Config:
        orm_mode = True

class CouponCreateSchema(CouponBaseSchema):
    pass


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
    is_used: bool = False

    class Config:
        orm_mode = True

class AppliedCouponResultSchema(BaseModel):
    final_price_after_discount: float
    discounted_amount: float
    used_code: str

class CodeRelatedSchema(BaseModel):
    code: str 
class ApplyCouponSchema(BaseModel):
    total_price: float 
class RedeemCouponSchema(CodeRelatedSchema):
    pass