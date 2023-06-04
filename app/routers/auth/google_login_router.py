import json

import requests
from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.main import get_social_login_exception, raise_http_exception
from ...services import user_services
from ...utils.security import security

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("/google-login")
async def google_auth(access_token: str, db: Session = Depends(db.get_db)):
    try:
        res = requests.get(
            f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
        )

        user_data = json.loads(res.text)

        user = user_services.find_user_with_email(user_data["email"], db)

        if user:
            if user_services.is_email_login(user.email, user.password):
                raise_http_exception(
                    api_msgs.EMAIL_ALREADY_REGISTERED_WITH_GOOGLE, status.HTTP_409_CONFLICT
                )

            if user_services.is_google_login(user.email, user.password):
                return user_services.gen_user_info_and_tokens(
                    user, user_services.calc_cart_length(user.cart.id, db) or 0
                )

        else:
            return user_services.create_google_login_user(user_data, db)

    except Exception as e:
        get_social_login_exception(e)
