from enum import Enum
from typing import Annotated, Generic, TypeVar

from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..database import db
from ..exceptions.http_exception import CustomHTTPException
from ..models.cart import cart_item_model
from ..schemas import user_schema
from ..schemas.user_schema import SupportedField, VerifiedValue
from ..services import product_services, user_services
from ..utils.dependencies import *
from ..utils.logger import logger
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'user',
    plural_prefix = 'users',
    tags = ['user']
)


@protected_singular.post(
    "/update",
    **get_path_decorator_settings(description= "Successfully update user data")
)
def update_user(
    req: Request,
    payload: user_schema.UserUpdateSchema,
    db: Session = Depends(db.get_db)
):

    (field,value) = jsonable_encoder(payload).values()
    #Convert value to python dict then get the values.
    #Can not do this when the data is of JSON format.
    #But you can actually just write payload.field XD 

    try:
        
        if field == SupportedField.VERIFIED:
            req.state.mydata.verified = int(value)
        
        elif field == SupportedField.LASTNAME:
            req.state.mydata.last_name = value
        elif field == SupportedField.FIRSTNAME:
            req.state.mydata.first_name = value
        #modify req.state.mydata == directly current user's data 

        db.commit()
        #then save it to the db

    except HTTPException as e:
        if type(e).__name__ == 'HTTPExceotion':
            raise e
        logger.error(e, exc_info=True)
        raise CustomHTTPException(detail= str(e))

@protected_singular.get(
    "/{user_id}", 
    response_model=user_schema.UserSchema
)
def get_user(user_id: str, db: Session = Depends(db.get_db)):
    user = user_services.find_user_with_id(user_id,db)
    return user


@protected_singular.post(
    "/reset-password",
    **get_path_decorator_settings(description= "Password has been successfully reset")
)
def reset_password(
    req: Request,
    payload: user_schema.CreatePasswordSchema,
    db: Session = Depends(db.get_db)
):
    try:
        req.state.mydata.password = payload.password
        db.commit()
    except Exception as e:
        raise CustomHTTPException(detail= str(e))
    


@public_singular.post(
    "/forgot-password", 
    **get_path_decorator_settings(description= "Password has been successfully reset")
)
async def forgot_password(
    payload: user_schema.EmailBaseSchema,
    db: Session = Depends(db.get_db)
):
    try:
        user = user_services.find_user_with_email(payload.email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User does not exist!'
            )
        
        link_params = {
            'user_id': user.id,
            'user_email': user.email,
            'link_type' : 'reset',
            'url_params' : 'reset-password/token'   
        }   
    
        await user_services.send_verify_or_reset_link(link_params)

        content = {
            "detail": "A verification email has been sent to your registered email address successfully."
        }
        return JSONResponse(
            content= content,
            status_code=200
        )

    except Exception as e:
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))

@protected_singular.post(
    "/upload-avatar", 
    **get_path_decorator_settings(description="Successfully upload your avatar!")
)
def get_uploaded_avatar_url(
    req: Request,
    payload: user_schema.UserUploadAvatarSchema,
    db: Session = Depends(db.get_db)
):
    try:
        req.state.mydata.upload_avatar = payload.url
        db.commit()

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
    

@protected_singular.post(
    "/add-to-cart", 
    **get_path_decorator_settings(description="Successfully add the product to the cart.")
)
def add_to_cart(
    req: Request,
    payload: user_schema.AddToCartSchema,
    db: Session = Depends(db.get_db)
):
    try:

        user_cart = req.state.mydata.cart

        cart_item = user_services.get_item_from_user_cart(req, payload.product_id)
        
        if cart_item:
            cart_item.quantity += payload.qty
            
        else:
            product = product_services.find_product_with_id(payload.product_id, db)

            if not product:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail = api_msgs.PRODUCT_NOT_FOUND
                )

            new_cart_item = cart_item_model.CartItem(
                quantity= payload.qty,
                product_id = product.id, 
                cart_id = user_cart.id
            )

            db.add(new_cart_item)

            user_cart.cart_items.append(new_cart_item)

        db.commit()

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))



    




