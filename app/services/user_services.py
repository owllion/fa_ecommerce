from decouple import config
from fastapi import Depends, HTTPException, Request, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..database import db
from ..models.cart import cart_item_model
from ..models.user import user_model
from ..schemas import email_schema, user_schema
from ..utils import security
from ..utils.email import email

from..constants import api_msgs



def find_user_with_email(
    email: str,
    db: Session = Depends(db.get_db)
):
    user = db.query(user_model.User).filter(user_model.User.email == EmailStr(email.lower())).first()
    
    return user


def find_user_with_id(
    id: str,
    db: Session = Depends(db.get_db)
):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    
    return user

def save_data_then_return(
    payload: user_schema.UserCreateSchema, 
    db: Session = Depends(db.get_db)
):
    new_user = user_model.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_updated_payload_data(payload: user_schema.UserCreateSchema):
    payload.password = security.hash_password(payload.password)
    payload.email = EmailStr(payload.email.lower())

    return payload 

def user_is_verified(verified: bool):
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Please verify your email address'
        )
    return True

def password_is_matched(payload_pwd: str, user_pwd: str):
    if not security.verify_password(payload_pwd, user_pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect Email or Password'
        )
    return True

async def send_verify_or_reset_link(params: email_schema.SendVerifyOrResetLinkSchema):
    user_id,user_email,link_type,url_params = params.values()

    token = security.create_token(user_id,'access')
    
    target_link = f'{config("FRONTEND_DEPLOY_URL")}/auth/{url_params}/{token}'

    await email.send_link({ 
        'type': link_type,
        'link': target_link, 
        'email': user_email 
    })

def get_item_from_user_cart(req: Request, product_id: str):

    cart_item = list(filter(lambda x: x.product_id == product_id, req.state.mydata.cart.cart_items))

    return cart_item[0] if cart_item else None


def get_user_cart_id(req: Request):
    return req.state.mydata.cart.id

def find_item_from_cart(req: Request, product_id: str, db: Session):
    user_cart_id = get_user_cart_id(req)
    print(user_cart_id,'這是id')
    print(product_id,'商品Id')

    cart_item =\
        db\
            .query(cart_item_model.CartItem)\
            .filter(
                cart_item_model.CartItem.product_id == product_id,
                cart_item_model.CartItem.cart_id == user_cart_id
            )\
            .first()
    print(cart_item,'這是cart_item')

    if not cart_item:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= api_msgs.CART_ITEM_NOT_FOUND
        )
    return cart_item

def delete_item(db: Session, cart_item: cart_item_model.CartItem):
    db.delete(cart_item)
    db.commit()

