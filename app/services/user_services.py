from decouple import config
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..database import db
from ..models.user import user_model
from ..schemas import email_schema, user_schema
from ..utils import security
from ..utils.email import email


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

