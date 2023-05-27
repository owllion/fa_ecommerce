from fastapi import Depends, HTTPException, status

from ...constants import api_msgs
from ...exceptions.custom_http_exception import CustomHTTPException
from ...exceptions.main import get_exception, raise_http_exception
from ...schemas import coupon_schema
from ...services import coupon_services, user_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="coupon", plural_prefix="coupons", tags=["coupon"]
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
        description="Successfully create a coupon", response_model=coupon_schema.CouponSchema
    )
)
def create_coupon(payload: coupon_schema.CouponCreateSchema, db: Session = Depends(db.get_db)):
    try:
        new_coupon = coupon_services.svc_create_coupon(payload, db)

        return new_coupon

    except Exception as e:
        get_exception(e)


@public_singular.get(
    "/{coupon_id}",
    **get_path_decorator_settings(
        description="Get the data of a single coupon.", response_model=coupon_schema.CouponSchema
    )
)
def get_coupon(coupon_id: str, db: Session = Depends(db.get_db)):
    try:
        coupon = coupon_services.find_coupon_with_id(coupon_id, db)

        if not coupon:
            raise_http_exception(api_msgs.COUPON_NOT_FOUND)

        return coupon

    except Exception as e:
        get_exception(e)


@public_plural.get(
    "/",
    **get_path_decorator_settings(
        description="Get the coupon list", response_model=list[coupon_schema.CouponSchema]
    )
)
def get_coupons(db: Session = Depends(db.get_db)):
    try:
        coupons = coupon_services.get_coupons(db)
        return coupons

    except Exception as e:
        get_exception(e)


@protected_plural.get(
    "/user",
    **get_path_decorator_settings(
        description="Get the specific user's coupon list",
        response_model=list[coupon_schema.CouponSchema],
    )
)
def get_user_coupons(req: Request, db: Session = Depends(db.get_db)):
    try:
        return req.state.mydata.coupons

    except Exception as e:
        get_exception(e)


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description="Successfully update the coupon.",
    )
)
def update_coupon(payload: coupon_schema.CouponUpdateSchema, db: Session = Depends(db.get_db)):
    try:
        coupon = coupon_services.find_coupon_with_id(payload.id, db)

        if not coupon:
            raise_http_exception(api_msgs.COUPON_NOT_FOUND)

        coupon_services.update_coupon_with(payload, coupon, db)

    except Exception as e:
        get_exception(e)


@protected_singular.delete(
    "/{coupon_id}/user/{user_id}",
    **get_path_decorator_settings(
        description="Successfully delete the coupon from user's coupon list.",
    )
)
def delete_user_coupon(user_id: str, coupon_id: str, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_id(user_id, db)
        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND)

        coupon = coupon_services.find_coupon_with_id(coupon_id, db)

        if not coupon:
            raise_http_exception(api_msgs.COUPON_NOT_FOUND)

        user.coupons.remove(coupon)

        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.delete(
    "/{coupon_id}",
    **get_path_decorator_settings(
        description="Successfully delete the coupon.",
    )
)
def delete_coupon(coupon_id: str, db: Session = Depends(db.get_db)):
    try:
        coupon = coupon_services.find_coupon_with_id(coupon_id, db)

        if not coupon:
            raise_http_exception(api_msgs.COUPON_NOT_FOUND)

        db.delete(coupon)
        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/apply-coupon",
    **get_path_decorator_settings(
        description="Successfully apply the coupon.",
        response_model=coupon_schema.AppliedCouponResultSchema,
    )
)
def apply_coupon(
    req: Request, payload: coupon_schema.ApplyCouponSchema, db: Session = Depends(db.get_db)
):
    try:
        coupon = coupon_services.get_coupon_from_req_user(req, payload.code)

        if not coupon:
            raise_http_exception(api_msgs.COUPON_NOT_FOUND)

        if coupon.is_used:
            raise_http_exception(api_msgs.COUPON_ALREADY_USED)

        (
            final_price_after_discount,
            discounted_amount,
        ) = coupon_services.get_final_price_and_discounted_amount(coupon, payload.total_price)

        return {
            "used_code": payload.code,
            "final_price_after_discount": final_price_after_discount,
            "discounted_amount": discounted_amount,
        }

    except Exception as e:
        get_exception(e)


@protected_singular.post(
    "/redeem-coupon", **get_path_decorator_settings(description="Successfully redeem a coupon.")
)
def redeem_coupon(
    req: Request, payload: coupon_schema.RedeemCouponSchema, db: Session = Depends(db.get_db)
):
    try:
        coupon = coupon_services.find_coupon_with_code(payload.code, db)

        if not coupon:
            raise_http_exception(api_msgs.COUPON_NOT_FOUND)

        coupon_services.add_coupon_to_user_coupon_list(req, coupon, db)

    except Exception as e:
        get_exception(e)
