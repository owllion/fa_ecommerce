from fastapi import FastAPI,HTTPException, Body,Header,Response,APIRouter,Depends,status,Request
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
from ..utils.dependencies import validate_token

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

    except Exception as e:
        raise CustomHTTPException(detail= str(e))

@protected_router.get("/{user_id}", response_model=user_schema.UserSchema)
def read_user(user_id: str, db: Session = Depends(db.get_db)):
    user = user_crud.find_user_with_id(user_id,db)
    return user



@protected_router.post(
    "/reset-password", 
    status_code= status.HTTP_200_OK,
    response_description= "Successfully reset password",
    response_model= None
)
def reset_password(
    req: Request,
    password: Annotated[str, Body()],
    db: Session = Depends(db.get_db)
):
    try:
        req.state.mydata.password = password
        db.commit()
    except Exception as e:
        raise CustomHTTPException(detail= str(e))




