from fastapi import FastAPI,HTTPException, Body,Header,APIRouter,Depends,status,Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from enum import Enum
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from typing import Generic,TypeVar
from pydantic import ValidationError

from ..utils.dependencies import *
from ..schemas import user_schema,item_schema
from ..database import db,crud
from ..database.crud import user_crud
from ..schemas.user_schema import SupportedFiled,VerifiedValue
from ..exceptions.http_exception import CustomHTTPException
from ..utils.router_settings import get_router_settings
from ..utils.logger import logger

protected_router = APIRouter(**get_router_settings(
  {
    'is_protected': True,
    'prefix': '/user',
    'tags': ['user'],
    'responses': {404: {"description": "Not found"}}
  }  
))

public_router = APIRouter(**get_router_settings(
  {
    'is_protected': False,
    'prefix': '/user',
    'tags': ['user'],
    'responses': {404: {"description": "Not found"}}
  }  
))


@protected_router.post(
    "/update", 
    status_code= status.HTTP_200_OK,
    response_description= "Successfully update",
    response_model= None
)
def update_user(
    req: Request,
    payload: user_schema.UserUpdateSchema,
    db: Session = Depends(db.get_db)
):

    (field,value) = jsonable_encoder(payload).values()
    #Convert value to python dict then get the values.
    #Can not do this when the data is of JSON format.

    try:
        if field == SupportedFiled.VERIFIED:
            req.state.mydata.verified = int(value)
        
        elif field == SupportedFiled.USERNAME:
            req.state.mydata.username = value
        #modify req.state.mydata == directly current user's data 

        db.commit()
        #then save it to the db

    except HTTPException as e:
        logger.error(e, exc_info=True)
        raise CustomHTTPException(detail= str(e.detail))

@protected_router.get("/{user_id}", response_model=user_schema.UserSchema)
def read_user(user_id: str, db: Session = Depends(db.get_db)):
    user = user_crud.find_user_with_id(user_id,db)
    return user


@protected_router.post(
    "/reset-password", 
    status_code= status.HTTP_200_OK,
    response_description= "Password has been successfully reset",
    response_model= None
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
    


@public_router.post(
    "/forgot-password", 
    status_code= status.HTTP_200_OK,
    response_description= "Password has been successfully reset",
    response_model= None
)
async def forgot_password(
    payload: user_schema.EmailBaseSchema,
    db: Session = Depends(db.get_db)
):
    try:
        user = user_crud.find_user_with_email(payload.email, db)
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
    
        await user_crud.send_verify_or_reset_link(link_params)

        content = {
            "detail": "A verification email has been sent to your registered email address successfully."
        }
        return JSONResponse(
            content= content,
            status_code=200
        )

    except HTTPException as e:
        raise CustomHTTPException(detail= str(e.detail))




