import json
from enum import Enum
from typing import Annotated

import requests
from authlib.integrations.starlette_client import OAuth, OAuthError
from decouple import config
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

# from starlette.requests import Request
from starlette.config import Config

from ...constants import api_msgs
from ...database import db
from ...exceptions.custom_http_exception import CustomHTTPException
from ...exceptions.get_exception import raise_http_exception
from ...schemas import user_schema
from ...services import user_services
from ...utils import security
from ...utils.dependencies import *
from ...utils.logger import logger
from ...utils.router_settings import get_path_decorator_settings
from ..product.product_router import get_products

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.get('/google-login')
async def google_auth(
    access_token: str,
    db: Session = Depends(db.get_db)
):
    try:
        res = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}")

        user_data = json.loads(res.text)

        print(user_data,'這是userdata')
        # print(user_data.email,'這是email .')
        print(user_data['email'],'這是email []')
        
        #建立新的user
        found_user = user_services.find_user_with_email(user_data['email'],db)

        if found_user:
            raise_http_exception(api_msgs.USER_ALREADY_EXISTS)
        
        payload = {
            'email' : user_data['email'],
            'first_name': user_data['given_name'],
            'last_name': user_data['family_name'] if 'family_name' in user_data else '',
            'upload_avatar': user_data['picture']
        }

        new_user = user_services.create_user_service(payload, db)
    
        return {
            'token': security.create_token(new_user.id,'access'),
            'refresh_token': security.create_token(new_user.id,'refresh'),
            'user': new_user,
        }

    except OAuthError as e:
        raise_http_exception(
            detail= e.description,
            status_code= status.HTTP_401_UNAUTHORIZED
        )



@router.post(
    '/register', 
    status_code= status.HTTP_201_CREATED,
    response_model= user_schema.RegisterResultSchema 
)
async def create_user(
    payload: user_schema.UserCreateSchema, 
    db: Session = Depends(db.get_db)
):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,detail='Account already exist'
            )

        new_user = user_services.create_user_service(payload,db)

        link_params = {
            'user_id': new_user.id,
            'user_email': new_user.email,
            'link_type' : 'verify',
            'url_params' : 'verify-email'   
        }
        
        await user_services.send_verify_or_reset_link(link_params)

        return_data = jsonable_encoder(new_user, by_alias=False)
        #改成易於serilize的格式(dict)

        # return_data.pop('password')

        print(return_data,'這是return data') 

        # return_data['token'] = security.create_token(new_user.id,'access')
        # return_data['refresh_token'] = security.create_token(new_user.id,'refresh')

        #註冊後根本不用船任何東西，因為沒認證email仕進不去的
        # return {
        #     'token': security.create_token(new_user.id,'access'),
        #     'refresh_token': security.create_token(new_user.id,'refresh'),
        #     'user': return_data,
        # }
        

    except Exception as e:
        logger.error(e, exc_info=True)

        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))



@router.post(
    '/login',
    status_code= status.HTTP_200_OK,
    response_model= user_schema.LoginResultSchema
)
def login(
    payload: user_schema.LoginUserSchema, 
    db: Session = Depends(db.get_db)
):
    try:
        user = user_services.find_user_with_email(payload.email, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User does not exist!'
            )


        if user_services.password_is_matched(payload.password, user.password) and user_services.user_is_verified(user.verified):
            # cart_length = db.query()
            return { 
                'token': security.create_token(user.id,"access"),
                'refresh_token': security.create_token(user.id,"refresh"),
                'user': user,
                'cart_length': len(user.cart.cart_items)     
            }


    except HTTPException as e:
        logger.error(e, exc_info=True)
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))


    


@router.post(
    '/refresh-token', response_model=user_schema.AccessAndRefreshTokenSchema
)
def get_refresh_token(
    payload: user_schema.TokenSchema,
    db: Session = Depends(db.get_db)
):
    try:
        decoded_data = security.decode_token(payload.token,'refresh',db)

        return {
            'token': security.create_token(
                decoded_data.id,
                'access'
            ),
            'refresh_token': security.create_token(
                decoded_data.id,
                'refresh'
            )
        }

    except Exception as e:
        logger.error(e, exc_info=True)
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))


@router.post(
    "/verify-token", 
    **get_path_decorator_settings(
        response_model= user_schema.RegisterResultSchema,
        description="Verify the token extracted from the link(email verification or google login callback)."
    )
)
def verify_token_from_link(
    payload: user_schema.TokenSchema,
    db: Session = Depends(db.get_db)
):
    try:
        decoded_data = security.decode_token(payload.token,'access',db)
        decoded_data.verified = 1
        db.commit()

        return {
            'token': security.create_token(
                decoded_data.id,
                'access'
            ),
            'refresh_token': security.create_token(
                decoded_data.id,
                'refresh'
            ),
            'user': decoded_data,
        }

    except Exception as e:
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))