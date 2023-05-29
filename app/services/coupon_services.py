from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..exceptions.main import get_exception, raise_http_exception
from ..models.coupon import coupon_model
from ..schemas import coupon_schema


def is_valid_coupon(expiry_date: datetime):
    print(expiry_date, "這是expire date")
    print(type(expiry_date), "這是expire date")

    expiry_datetime = datetime.strptime(expiry_date, "%Y-%m-%dT%H:%M:%S")

    if (expiry_datetime - datetime.now()).total_seconds() > 0:
        return True

    raise_http_exception(api_msgs.COUPON_EXPIRED)


def is_threshold_met(min_amount: float, total_price: float):
    if total_price > min_amount:
        return True

    raise_http_exception(api_msgs.MINIMUM_THRESHOLD_NOT_MET)


def get_price_and_discount(discount_type: str, total_price: float, amount: float):
    final_price = (
        total_price - amount
        if discount_type == "fix_amount"
        else round(total_price * (amount * 0.01))
    )

    return {
        "final_price_after_discount": final_price,
        "discounted_amount": total_price - final_price,
    }


def find_coupon_with_id(id: str, db: Session):
    coupon = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.id == id).first()

    return coupon


def find_coupon_with_code(code: str, db: Session):
    coupon = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.code == code).first()

    return coupon


def get_coupons(db: Session):
    return db.query(coupon_model.Coupon).all()


def get_user_coupons(user_id: str, db: Session):
    coupons = db.query(coupon_model.Coupon).filter(coupon_model.Coupon.user_id == user_id).all()

    return coupons


def get_coupon_from_req_user(req: Request, code: str):
    coupon = list(filter(lambda x: x.code == code, req.state.mydata.coupons))

    return coupon[0] if coupon else None


def get_coupon_or_raise_not_found(req: Request, code: str, db: Session):
    coupon = get_coupon_from_req_user(req, code)

    if not coupon:
        raise_http_exception(api_msgs.COUPON_NOT_FOUND)

    return coupon


def get_final_price_and_discounted_amount(coupon: coupon_model.Coupon, total_price: float):
    COUPON_FIELDS = ("expiry_date", "minimum_amount", "discount_type", "amount")

    expiry_date, minimum_amount, discount_type, amount = [
        jsonable_encoder(coupon)[k] for k in COUPON_FIELDS
    ]

    if is_valid_coupon(expiry_date) and is_threshold_met(minimum_amount, total_price):
        final_price_after_discount, discounted_amount = get_price_and_discount(
            discount_type, total_price, amount
        ).values()

    return (final_price_after_discount, discounted_amount)


def add_coupon_to_user_coupon_list(req: Request, coupon: coupon_model.Coupon, db: Session):
    found_coupon = get_coupon_from_req_user(req, coupon.code)

    if found_coupon:
        raise_http_exception(api_msgs.COUPON_ALREADY_EXISTS)

    req.state.mydata.coupons.append(coupon)
    db.commit()


def svc_create_coupon(payload: coupon_schema.CouponCreateSchema, db: Session):
    new_coupon = coupon_model.Coupon(**payload.dict())
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return new_coupon


def update_coupon_with(
    payload: coupon_schema.CouponUpdateSchema, coupon: coupon_model.Coupon, db: Session
):
    data = payload.dict(exclude_unset=True)
    # convert pydantic instance to dictionary for using py's items()

    for field, value in data.items():
        if hasattr(coupon, field):
            setattr(coupon, field, value)

    db.commit()
