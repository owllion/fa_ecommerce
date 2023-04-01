from fastapi import FastAPI,HTTPException, Body,Header,Response,APIRouter,Depends,status
from sqlalchemy.orm import Session
from enum import Enum
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from typing import Generic,TypeVar

from ..utils.dependencies import *
from ..schemas import user_schema,item_schema
from ..database import db,crud
from ..database.crud import user_crud
from ..schemas.user_schema import SupportedFiled

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# @router.post("/update", status_code=status.HTTP_200_OK)
# def update_user(id: str , username: str, db: Session = Depends(db.get_db)):
#     user = user_crud.find_user_with_id(id,db)
#     test = 'verified'
#     user[test] = username
#     db.commit()

@router.post(
    "/update", 
    status_code= status.HTTP_200_OK,
    response_description= "Successfully update",
    response_model= None
)
def update_user(
    payload: user_schema.UserUpdateSchema,
    db: Session = Depends(db.get_db)
):

    (id,field,value) = jsonable_encoder(payload).values()
    print(id,field,value)
    user = user_crud.find_user_with_id(id,db)

    if field == SupportedFiled.USERNAME:
        if not type(value) is bool: 
            raise TypeError('value for verified field must be boolean') 
    
        user.verified = value
    
    elif field == SupportedFiled.VERIFIED:
        user.username = value

    db.commit()
   

@router.get("/{user_id}", response_model=user_schema.UserSchema)
def read_user(user_id: str, db: Session = Depends(db.get_db)):
    user = user_crud.find_user_with_id(user_id,db)
    return user


# @router.post("/{user_id}/items/", response_model=item_schema.Item)
# def create_item_for_user(
#     user_id: str, item: item_schema.ItemCreate, db: Session = Depends(db.get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)

