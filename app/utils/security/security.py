from datetime import datetime, timedelta

from decouple import config
from fastapi import status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...exceptions.main import raise_http_exception
from ...services import user_services

# expire time
ACCESS_TOKEN_EXPIRES_IN = config("ACCESS_TOKEN_EXPIRES_IN", cast=int)
REFRESH_TOKEN_EXPIRES_IN = config("REFRESH_TOKEN_EXPIRES_IN", cast=int)
RESET_PWD_EXPIRES_IN = config("RESET_PWD_EXPIRES_IN", cast=int)
VALIDATE_EMAIL_EXPIRES_IN = config("VALIDATE_EMAIL_EXPIRES_IN", cast=int)

secrets = {
    "access": config("JWT_SECRET"),
    "refresh": config("REFRESH_SECRET"),
    "reset_pwd": config("RESET_PWD_SECRET"),
    "validate_email": config("VALIDATE_EMAIL_SECRET"),
}

time_deltas = {
    "access": timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
    "refresh": timedelta(days=REFRESH_TOKEN_EXPIRES_IN),
    "reset_pwd": timedelta(minutes=RESET_PWD_EXPIRES_IN),
    "validate_email": timedelta(minutes=VALIDATE_EMAIL_EXPIRES_IN),
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def is_hashed_password(password: str):
    return pwd_context.identify(password) is not None


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_secret(token_type: str):
    return secrets.get(token_type)


def create_token(user_id: str, token_type: str):
    token_timedelta = time_deltas[token_type]

    expire = datetime.utcnow() + token_timedelta
    token = jwt.encode(
        claims={"exp": expire, "user_id": user_id},
        key=get_secret(token_type),
        algorithm=config("JWT_ALGORITHM"),
    )

    return token


def decode_token(token: str, token_type: str, db: Session):
    try:
        payload = jwt.decode(
            token,
            get_secret(token_type),
            algorithms=[config("JWT_ALGORITHM")],
        )

        user = user_services.find_user_with_id(payload["user_id"], db)

        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND, status.HTTP_401_UNAUTHORIZED)

        return user

    except ExpiredSignatureError:
        raise_http_exception(api_msgs.TOKEN_EXPIRED, status.HTTP_401_UNAUTHORIZED)
    except JWTError as e:
        raise_http_exception(api_msgs.MALFORMED_TOKEN)
