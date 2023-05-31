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

        # email login
        if user.email and user.password:
            raise_http_exception(
                api_msgs.EMAIL_ALREADY_REGISTERED_WITH_GOOGLE, status.HTTP_409_CONFLICT
            )

        # google login
        if user.email and not user.password:
            return user_services.gen_user_info_and_tokens(
                user, user_services.calc_cart_length(user.cart.id, db)
            )

        # create new user
        payload = {
            "email": user_data["email"],
            "first_name": user_data["given_name"],
            "last_name": user_data["family_name"] if "family_name" in user_data else "",
            "upload_avatar": user_data["picture"],
            "verified": True,
        }

        new_user = user_services.svc_create_user(payload, db)

        user_services.create_cart(new_user.id, db)
        user_services.issue_coupons(new_user, db)

        return user_services.gen_user_info_and_tokens(new_user, cart_length=0)

    except Exception as e:
        get_social_login_exception(e)
