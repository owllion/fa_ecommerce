from fastapi import FastAPI,HTTPException, Body,Header,Response,APIRouter,Depends,status
from enum import Enum
from pydantic import BaseModel,Field,EmailStr
from typing import Annotated
from decouple import config
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from ..utils.dependencies import *
from ..utils import security

from ..schemas import user_schema,item_schema
from ..models import user_model

from ..database import db,crud
from ..database.crud import user_crud



ACCESS_TOKEN_EXPIRES_IN = config('ACCESS_TOKEN_EXPIRES_IN')
REFRESH_TOKEN_EXPIRES_IN = config('REFRESH_TOKEN_EXPIRES_IN')

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post('/register', status_code= status.HTTP_201_CREATED, response_model= user_schema.UserSchema)
async def create_user(payload: user_schema.UserCreateSchema, db: Session = Depends(db.get_db)):

    user = user_crud.find_user_with_email(payload.email, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,detail='Account already exist')
    
    payload = user_crud.get_updated_payload_data(payload)
    print(payload,'this is payload')

    new_user = user_model.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



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
        user['access_token'] = access_token
        user['refresh_token'] - refresh_token

        return user