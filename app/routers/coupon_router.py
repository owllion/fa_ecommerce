from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..constants import api_msgs
from ..exceptions.http_exception import CustomHTTPException
from ..schemas import coupon_schema
from ..services import coupon_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'coupon',
    plural_prefix = 'coupons',
    tags = ['coupon']
)

@protected_singular.post(
    "/", 
    **get_path_decorator_settings(
        description= "Successfully create a coupon",
        response_model= coupon_schema.CouponSchema
    )
)
def create_coupon(payload: coupon_schema.CouponCreateSchema, db: Session = Depends(db.get_db)):
    
    try:
        new_coupon = coupon_services.save_to_db_then_return(payload,db)
        
        return new_coupon


    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@public_singular.get(
    "/{coupon_id}",
    **get_path_decorator_settings(
        description= "Get the data of a single coupon.",
        response_model= coupon_schema.CouponSchema
    )
)
def get_coupon(coupon_id: str, db:Session = Depends(db.get_db)):
    try:
        coupon = coupon_services.find_coupon_with_id(coupon_id,db)

        if not coupon: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.COUPON_NOT_FOUND
            )
        
        return coupon
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
    
@public_plural.get(
    "/",
    **get_path_decorator_settings(
        description= "Get the coupon list",
        response_model= list[coupon_schema.CouponSchema]
    )
)
def get_coupons(db:Session = Depends(db.get_db)):
    try:
        coupons = coupon_services.get_coupons(db)

        return coupons
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
    


@protected_plural.get(
    "/user",
    **get_path_decorator_settings(
        description= "Get the specific user's coupon list",
        response_model= list[coupon_schema.CouponSchema]
    )
)
def get_user_coupons(req: Request, db: Session = Depends(db.get_db)):
    try:
        return req.state.mydata.coupons
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description= "Successfully update the coupon.",
    )
)
def update_coupon(
    payload: coupon_schema.CouponUpdateSchema,
    db:Session = Depends(db.get_db)
):
    try:
        coupon = coupon_services.find_coupon_with_id(payload.id,db)

        if not coupon: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.COUPON_NOT_FOUND
            )
        
        coupon_services.update_coupon_with(payload,coupon,db)
        
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.delete(
    "/{coupon_id}",
    **get_path_decorator_settings(
        description= "Successfully delete the coupon.",
    )
)
def delete_coupon(coupon_id: str, db: Session = Depends(db.get_db)):
    try:
        coupon = coupon_services.find_coupon_with_id(coupon_id,db)

        if not coupon: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.COUPON_NOT_FOUND
            )
        
        db.delete(coupon)
        
        db.commit()
        
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.post(
    "/apply-coupon",
    **get_path_decorator_settings(
        description= "Successfully apply the coupon.",
        response_model= coupon_schema.AppliedCouponResultSchema
    )
)
def apply_coupon(
    req: Request,
    payload: coupon_schema.ApplyCouponSchema,
    db: Session = Depends(db.get_db)
):
    try:
        coupon = coupon_services.get_coupon_from_req_user(req, payload.code)

        if not coupon:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.COUPON_NOT_FOUND
            )

        final_price_after_discount,discounted_amount = coupon_services.get_final_price_and_discounted_amount(coupon,payload.total_price)

        return {
            "used_code": payload.code,
            "final_price_after_discount": final_price_after_discount,
            "discounted_amount": discounted_amount
        }
        
    except Exception as e:
        if isinstance(e, (HTTPException,)): 
            raise e
        raise CustomHTTPException(detail= str(e))
    

@protected_singular.post(
    "/redeem-coupon",
    **get_path_decorator_settings(
        description= "Successfully redeem a coupon."
    )
)
def redeem_coupon(
    req: Request,
    payload: coupon_schema.RedeemCouponSchema,
    db: Session = Depends(db.get_db)
):
    try:
        coupon = coupon_services.find_coupon_with_code(payload.code, db)

        if not coupon:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.COUPON_NOT_FOUND
            )
        
        coupon_services.add_coupon_to_user_coupon_list(req,coupon, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)): 
            raise e
        raise CustomHTTPException(detail= str(e))
    

