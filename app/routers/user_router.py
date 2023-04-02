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

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(validate_token)],
    responses={404: {"description": "Not found"}},
)

@router.post(
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

        db.commit()

    except:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Something went wrong!"
        )
        




   

@router.get("/{user_id}", response_model=user_schema.UserSchema)
def read_user(user_id: str, db: Session = Depends(db.get_db)):
    user = user_crud.find_user_with_id(user_id,db)
    return user


# @router.post("/{user_id}/items/", response_model=item_schema.Item)
# def create_item_for_user(
#     user_id: str, item: item_schema.ItemCreate, db: Session = Depends(db.get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)

