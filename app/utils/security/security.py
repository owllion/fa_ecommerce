from datetime import datetime, timedelta
from typing import Annotated

from decouple import config
from fastapi import Depends, FastAPI, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...exceptions.main import raise_http_exception
from ...services import user_services

# from ..common.logger import logger

ACCESS_TOKEN_EXPIRES_IN = config("ACCESS_TOKEN_EXPIRES_IN", cast=int)
REFRESH_TOKEN_EXPIRES_IN = config("REFRESH_TOKEN_EXPIRES_IN", cast=int)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def is_hashed_password(password: str):
    return pwd_context.identify(password) is not None


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_token(user_id: str, token_type: str):
    token_timedelta = (
        timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
        if token_type == "access"
        else timedelta(days=REFRESH_TOKEN_EXPIRES_IN)
    )

    expire = datetime.utcnow() + token_timedelta

    token = jwt.encode(
        claims={"exp": expire, "user_id": user_id},
        key=config("JWT_SECRET") if token_type == "access" else config("REFRESH_SECRET"),
        algorithm=config("JWT_ALGORITHM"),
    )

    return token


def decode_token(token: str, token_type: str, db: Session):
    try:
        payload = jwt.decode(
            token,
            config("JWT_SECRET") if token_type == "access" else config("REFRESH_SECRET"),
            algorithms=[config("JWT_ALGORITHM")],
        )
        user = user_services.find_user_with_id(payload["user_id"], db)

        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND, status.HTTP_401_UNAUTHORIZED)

        return user

    except ExpiredSignatureError:
        raise_http_exception(api_msgs.TOKEN_EXPIRED, status.HTTP_401_UNAUTHORIZED)
    except JWTError as e:
        # logger.error(e, exc_info=True)
        raise raise_http_exception(api_msgs.MALFORMED_TOKEN)
