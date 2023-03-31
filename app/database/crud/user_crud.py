from ...database import db
from ...models import user_model
from pydantic import EmailStr
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session

from ...schemas import user_schema
from ...utils import security

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


