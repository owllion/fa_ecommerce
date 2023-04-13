from sqlalchemy.orm import Session

from ..models.coupon import coupon_model
from ..schemas import coupon_schema


def find_coupon_with_id(
    id: str,
    db: Session
):
    coupon = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.id == id).first()

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