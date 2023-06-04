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
        if len(values) < 2 and values.get("id"):
            raise ValueError("At least one attribute other than 'id' must be provided.")

        for attr in values:
            if attr != "id":
                if attr not in base_keys:
                    raise ValueError(f"You've passed a non-existing attribute: {attr}")
        return values


class CouponSchema(CouponBaseSchema):
    id: str

    class Config:
        orm_mode = True


class AppliedCouponResultSchema(BaseModel):
    final_price_after_discount: float
    discounted_amount: float
    used_code: str


class CodeSchema(BaseModel):
    code: str


class ApplyCouponSchema(CodeSchema):
    total_price: float


class RedeemCouponSchema(BaseModel):
    coupon_id: str


# baseSchema就是update時也可以改的，但基本上沒有，誰會要改這，直接就createschema吧
class UserCouponCreateSchema(BaseModel):
    user_id: str
    coupon_id: str
    is_used: bool
