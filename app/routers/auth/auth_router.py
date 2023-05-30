from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...constants import api_msgs, constants
from ...database import db
from ...exceptions.main import CustomHTTPException, get_exception, raise_http_exception
from ...schemas import user_schema
from ...services import user_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)
from ...utils.security import security

_, _, _, public_singular = get_router_settings(
    singular_prefix="auth", plural_prefix="auth", tags=["auth"]
)


@public_singular.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: user_schema.UserCreateSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if user:
            raise_http_exception(api_msgs.ACCOUNT_ALREADY_EXISTS, status.HTTP_409_CONFLICT)

        new_user = user_services.svc_create_user(payload, db)
        user_services.create_cart(new_user.id, db)
        user_services.issue_coupons(new_user, db)

        link_params = {
            "user_id": new_user.id,
            "user_email": new_user.email,
            "link_type": constants.URLLinkType.VERIFY,
            "token_type": constants.TokenType.VALIDATE_EMAIL,
            "url_params": constants.URLParams.VERIFY_EMAIL,
        }

        await user_services.send_link(link_params)

    except Exception as e:
        get_exception(e)


@public_singular.post("/login", response_model=user_schema.LoginResultSchema)
def login(payload: user_schema.LoginUserSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND)
        print(user, "這是uesr")
        if user_services.password_is_matched(
            payload.password, user.password
        ) and user_services.user_is_verified(user.verified):
            return {
                "token": security.create_token(user.id, "access"),
                "refresh_token": security.create_token(user.id, "refresh"),
                "user": user,
                "cart_length": len(user.cart.cart_items),
            }

    except Exception as e:
        get_exception(e)


@public_singular.post("/refresh-token", response_model=user_schema.AccessAndRefreshTokenSchema)
def get_refresh_token(payload: user_schema.TokenSchema, db: Session = Depends(db.get_db)):
    try:
        decoded_data = security.decode_token(payload.token, "refresh", db)

        return {
            "token": security.create_token(decoded_data.id, "access"),
            "refresh_token": security.create_token(decoded_data.id, "refresh"),
        }

    except Exception as e:
        get_exception(e)


@public_singular.post(
    "/verify-token",
    **get_path_decorator_settings(
        response_model=user_schema.RegisterResultSchema,
        description="Verify the token extracted from the link(email verification or google login callback).",
    )
)
def verify_token_from_link(payload: user_schema.TokenSchema, db: Session = Depends(db.get_db)):
    try:
        decoded_data = security.decode_token(payload.token, "access", db)

        decoded_data.verified = 1

        db.commit()

        return {
            "token": security.create_token(decoded_data.id, "access"),
            "refresh_token": security.create_token(decoded_data.id, "refresh"),
            "user": decoded_data,
        }

    except Exception as e:
        get_exception(e)


@public_singular.post(
    "/check-token",
    **get_path_decorator_settings(
        response_model=None,
        description="Check if the token retrieved from the link is valid",
    )
)
def check_if_token_is_valid(payload: user_schema.TokenSchema):
    try:
        security.decode_token(payload.token, constants.TokenType.RESET_PWD, db)

        return {"is_valid": True}

    except Exception as e:
        get_exception(e)
        return {"is_valid": False}
