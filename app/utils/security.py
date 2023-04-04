from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError,ExpiredSignatureError,jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from decouple import config
from sqlalchemy.orm import Session

from ..database.crud import user_crud
from ..database import db


ACCESS_TOKEN_EXPIRES_IN = config('ACCESS_TOKEN_EXPIRES_IN',cast=int)
REFRESH_TOKEN_EXPIRES_IN = config('REFRESH_TOKEN_EXPIRES_IN',cast=int)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_token(user_id: str, token_type: str):
    token_timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN) if token_type == 'access' else timedelta(days=REFRESH_TOKEN_EXPIRES_IN)

    expire = datetime.utcnow() + token_timedelta
    
    token = jwt.encode(
        claims = {
            "exp": expire, 
            "user_id":user_id
        },
        key = config('JWT_SECRET') if token_type == 'access' else config('REFRESH_SECRET'), 
        algorithm= config('JWT_ALGORITHM')
    )

    return token

def decode_token(
    token: str, 
    token_type: str, 
    db:Session
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Malformed token, please provide a valid token",
    )
    try:
        payload = jwt.decode(
            token, 
            config('JWT_SECRET') if token_type == 'access' else config('REFRESH_SECRET'),
            algorithms=[config('JWT_ALGORITHM')]
        )
        user = user_crud.find_user_with_id(payload['user_id'], db)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail="User does not exist."
        )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired."
        )
    except JWTError:
        raise credentials_exception
