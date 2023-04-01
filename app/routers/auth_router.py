from fastapi import FastAPI,HTTPException,APIRouter,Depends,status
from enum import Enum
#from pydantic import BaseModel,Field,EmailStr
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from ..utils.dependencies import *
from ..utils import security

from ..schemas import user_schema
from ..models import user_model

from ..database import db
from ..database.crud import user_crud

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

    user = user_crud.find_user_with_email(payload.email, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,detail='Account already exist')
    
    payload = user_crud.get_updated_payload_data(payload)

    new_user = user_crud.save_data_then_return(payload,db)

    return_data = jsonable_encoder(new_user) 

    return_data['access_token'] = security.create_token(new_user.id,'access')
    return_data['refresh_token'] = security.create_token(new_user.id,'refresh')

    return return_data



@router.post('/login',response_model= user_schema.UserWithTokenSchema)
def login(
    payload: user_schema.LoginUserSchema, 
    db: Session = Depends(db.get_db)
):
    user = user_crud.find_user_with_email(payload.email, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User does not exist!'
        )

    if user_crud.password_is_matched(payload.password, user.password) and user_crud.user_is_verified(user.verified):
        access_token = security.create_token(user.id,"access")
        refresh_token = security.create_token(user.id,"refresh")
        user = jsonable_encoder(user)
        user['access_token'] = access_token
        user['refresh_token'] = refresh_token

        return user
    
@router.post('/refresh-token')
def get_refresh_token(
    token: str,
    db: Session = Depends(db.get_db)
):
    decoded_data = security.decode_token(token,'refresh',db)

    return {
        'access_token': security.create_token(
            decoded_data.user_id,
            'access'
        ),
        'refresh_token': security.create_token(
            decoded_data.user_id,
            'refresh'
        )
    }
        
































