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
            if user_services.is_google_login(user.email, user.password):
                raise_http_exception(api_msgs.EMAIL_ALREADY_REGISTERED_WITH_GOOGLE)

            if user_services.is_email_login(user.email, user.password):
                raise_http_exception(api_msgs.ACCOUNT_ALREADY_EXISTS, status.HTTP_409_CONFLICT)
        else:
            await user_services.create_email_login_user(payload, db)

    except Exception as e:
        get_exception(e)


@public_singular.post("/login", response_model=user_schema.LoginResultSchema)
def login(payload: user_schema.LoginUserSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND)
        if user_services.password_is_matched(
            payload.password, user.password
        ) and user_services.user_is_verified(user.verified):
            return {
                "token": security.create_token(user.id, "access"),
                "refresh_token": security.create_token(user.id, "refresh"),
                "user": user,
                "cart_length": user_services.calc_cart_length(user.cart.id, db) or 0,
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
    "/check-verify-token",
    **get_path_decorator_settings(
        response_model=user_schema.RegisterResultSchema,
        description="Verify the token extracted from the link(email verification or google login callback).",
    )
)
def verify_token(payload: user_schema.TokenSchema, db: Session = Depends(db.get_db)):
    try:
        decoded_data = security.decode_token(payload.token, constants.TokenType.VALIDATE_EMAIL, db)

        decoded_data.verified = 1

        db.commit()

        return user_services.gen_user_info_and_tokens(decoded_data, cart_length=0)

    except Exception as e:
        get_exception(e)


@public_singular.post(
    "/check-reset-token",
    **get_path_decorator_settings(
        response_model=None,
        description="Check if the reset_pwd token is still valid or not.",
    )
)
def check_token(payload: user_schema.TokenSchema, db: Session = Depends(db.get_db)):
    try:
        security.decode_token(payload.token, constants.TokenType.RESET_PWD, db)

        return {"is_valid": True}

    except Exception as e:
        get_exception(e)
        return {"is_valid": False}


@public_singular.post(
    "/check-account",
    **get_path_decorator_settings(
        description="Check if the account already exists.",
    )
)
def check_if_account_exists(
    payload: user_schema.EmailBaseSchema, db: Session = Depends(db.get_db)
):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if user:
            if user_services.is_google_login(user.email, user.password):
                raise_http_exception(api_msgs.EMAIL_ALREADY_REGISTERED_WITH_GOOGLE)

            if user_services.is_email_login(user.email, user.password):
                return {"has_account": True}

        return {"has_account": False}

    except Exception as e:
        get_exception(e)


@public_singular.post(
    "/send-email",
    **get_path_decorator_settings(
        description="Send email to specific email address.",
    )
)
async def send_email(payload: user_schema.SendEmailSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND)
        link_type = (
            constants.URLLinkType.RESET
            if "reset" in payload.token_type
            else constants.URLLinkType.VERIFY
        )
        url_params = (
            constants.URLParams.RESET_PWD
            if "reset" in payload.token_type
            else constants.URLParams.VERIFY_EMAIL
        )

        link_params = {
            "user_id": user.id,
            "user_email": user.email,
            "link_type": link_type,
            "token_type": payload.token_type,
            "url_params": url_params,
        }

        await user_services.send_link(link_params)

    except Exception as e:
        get_exception(e)
