from ...database import db
from ...models import user_model
from pydantic import EmailStr
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session

from ...schemas import user_schema
from ...utils import security

def find_user_with(email: str, db: Session = Depends(db.get_db)):
    print(email,'拿到的email')
    print(EmailStr(email.lower()),'轉換過的email')
    user = db.query(user_model.User).filter(
        user_model.User.email == EmailStr(email.lower())).first()
    print(user,"只到的user")
    return user

def get_updated_payload_data(payload: user_schema.UserCreateSchema):
    payload.password = security.hash_password(payload.password)
    payload.email = EmailStr(payload.email.lower())

    return payload 