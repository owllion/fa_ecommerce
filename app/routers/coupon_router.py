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
    


@public_plural.get(
    "/user/{user_id}",
    **get_path_decorator_settings(
        description= "Get the specific user's coupon list",
        response_model= list[coupon_schema.CouponSchema]
    )
)
def get_user_coupons(user_id: str, db: Session = Depends(db.get_db)):
    try:
        coupons = coupon_services.get_user_coupons(user_id,db)

        return coupons
          
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
    code: str, 
    total_price: float, 
    db: Session = Depends(db.get_db)
):
    #1.找到coupon 2.確認有沒有過期 3.確認金額有無到達門檻 4.都符合才去用getPriceAndDiscount獲得discountTotal, discount

    coupon = coupon_services.find_coupon_with_code(code)

    if not coupon:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= api_msgs.COUPON_NOT_FOUND
        )
    
    expiry_date,minimum_amount,discount_type,amount = jsonable_encoder(coupon).values()

    if \
        coupon_services.is_valid_coupon(expiry_date)\
        and\
        coupon_services.is_threshold_met(minimum_amount,total_price):
        

    

