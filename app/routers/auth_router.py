from enum import Enum
#from pydantic import BaseModel,Field,EmailStr
from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..database import db
from ..exceptions.http_exception import CustomHTTPException
from ..models import user_model
from ..schemas import user_schema
from ..services import user_services
from ..utils import security
from ..utils.dependencies import *
from ..utils.email import email
from ..utils.logger import logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post('/register', 
             status_code= status.HTTP_201_CREATED, response_model= user_schema.UserWithTokenSchema
        )
async def create_user(
    payload: user_schema.UserCreateSchema, 
    db: Session = Depends(db.get_db)
):
    user = user_services.find_user_with_email(payload.email, db)
    

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,detail='Account already exist'
        )

    new_user = user_services.save_data_then_return(payload,db)

    link_params = {
        'user_id': new_user.id,
        'user_email': new_user.email,
        'link_type' : 'verify',
        'url_params' : 'verify-email'   
    }
    
    await user_services.send_verify_or_reset_link(link_params)

    return_data = jsonable_encoder(new_user) 

    return_data['access_token'] = security.create_token(new_user.id,'access')
    return_data['refresh_token'] = security.create_token(new_user.id,'refresh')

    return return_data



@router.post('/login',response_model= user_schema.UserWithTokenSchema)
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
            access_token = security.create_token(user.id,"access")
            refresh_token = security.create_token(user.id,"refresh")
            user = jsonable_encoder(user)
            user['access_token'] = access_token
            user['refresh_token'] = refresh_token

            return user
        
    except HTTPException as e:
        logger.error(e, exc_info=True)
        raise CustomHTTPException(detail= str(e.detail))

    
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
    except HTTPException as e:
        logger.error(e, exc_info=True)
        raise CustomHTTPException(detail= str(e.detail))






























