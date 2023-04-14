import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..models.coupon import coupon_model
from ..schemas import coupon_schema


def is_valid_coupon(expiry_date: datetime):
    print(expiry_date,'這是expire date')
    print(type(expiry_date),'這是expire date')
    if expiry_date - datetime.datetime.now() > 0: return True

    raise HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail= api_msgs.COUPON_EXPIRED
    )

def is_threshold_met(min_amount: float, total_price: float):
    if total_price > min_amount: return True
    
    raise HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail= api_msgs.MINIMUM_THRESHOLD_NOT_MET
    )

def get_price_and_discount(
  discount_type: str,
  total_price: float,
  amount: float 
):

    final_price = total_price - amount if discount_type == "fix_amount" else round(total_price * (amount * 0.01))

    return {
        "final_price_after_discount": final_price,
        "discounted_amount": total_price - final_price,
    }

def find_coupon_with_id(
    id: str,
    db: Session
):
    coupon = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.id == id).first()

    return coupon

def find_coupon_with_code(
    code: str,
    db: Session
):
    coupon = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.code == code).first()

    return coupon

def get_coupons(db: Session):
    coupons = db.query(coupon_model.Coupon).all()
    return coupons

def get_user_coupons(user_id: str,db: Session):
    coupons = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.user_id == user_id).all()
    return coupons

def save_to_db_then_return(
    payload: coupon_schema.CouponCreateSchema,
    db: Session
):
    new_coupon = coupon_model.Coupon(**payload.dict())
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return new_coupon

def update_coupon_with(
    payload: coupon_schema.CouponUpdateSchema,
    coupon: coupon_model.Coupon,
    db: Session
):

    data = payload.dict(exclude_unset=True)
    #convert pydantic instance to dictionary to use py's items()

    for field, value in data.items():
        if hasattr(coupon, field) :
            setattr(coupon, field, value)
        
    db.commit()

