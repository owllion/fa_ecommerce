from enum import Enum

#from pydantic import BaseModel,Field,EmailStr
from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..database import db
from ..exceptions.http_exception import CustomHTTPException
from ..models.user import user_model
from ..schemas import user_schema
from ..services import user_services
from ..utils import security
from ..utils.dependencies import *
from ..utils.logger import logger
from ..utils.router_settings import get_path_decorator_settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


    # response_model= user_schema.UserWithTokenSchema,
    # response_model_by_alias=False
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

        print(payload, '這是payload')
        new_user = user_services.save_data_then_return(payload,db)

        link_params = {
            'user_id': new_user.id,
            'user_email': new_user.email,
            'link_type' : 'verify',
            'url_params' : 'verify-email'   
        }
        
        await user_services.send_verify_or_reset_link(link_params)

        return_data = jsonable_encoder(new_user, by_alias=False)

        # return_data.pop('password')

        print(return_data,'這是return data') 

        # return_data['token'] = security.create_token(new_user.id,'access')
        # return_data['refresh_token'] = security.create_token(new_user.id,'refresh')


        return {
            'token': security.create_token(new_user.id,"access"),
            'refresh_token': security.create_token(new_user.id,"refresh"),
            'user': return_data,
        }

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
            return { 
                'token': security.create_token(user.id,"access"),
                'refresh_token': security.create_token(user.id,"refresh"),
                'user': user,
                'cartLength': 0      
            }


    except HTTPException as e:
        logger.error(e, exc_info=True)
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))

    
@router.post('/refresh-token', response_model=user_schema.AccessAndRefreshTokenSchema)
def get_refresh_token(
    payload: user_schema.TokenSchema,
    db: Session = Depends(db.get_db)
):
    try:
        decoded_data = security.decode_token(payload.token,'refresh',db)

        return {
            'access_token': security.create_token(
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
    "/verify-email-token", 
    **get_path_decorator_settings(
        response_model= user_schema.RegisterResultSchema,
        description="Verify user email with the token extracted from the link provided in the email. Returns a success message if the token is valid."
    )
)
def verify_token_from_email_link(
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


    
    
































