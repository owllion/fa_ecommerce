import json

from decouple import config
from fastapi import APIRouter, Depends, HTTPException, Request, status
from requests_oauthlib import OAuth2Session
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.main import get_social_login_exception, raise_http_exception
from ...schemas import auth_schema
from ...services import user_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import get_path_decorator_settings
from ...utils.security import security

client_id = config("GITHUB_CLIENT_ID")
client_secret = config("GITHUB_CLIENT_SECRET")

github = OAuth2Session(client_id)

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("/github-login")
async def github_login():
    url = github.authorization_url(authorization_base_url)
    print(url, "這是url")
    return url[0]


@router.post("/github-auth")
async def github_auth(payload: auth_schema.SocialLoginSchema, db: Session = Depends(db.get_db)):
    try:
        github.fetch_token(
            token_url, client_secret=client_secret, authorization_response=payload.reqUrl
        )

        res = github.get("https://api.github.com/user")

        user_data = json.loads(res.text)

        user = user_services.find_user_with_github_username(user_data["login"], db)

        if user:
            return user_services.gen_user_info_and_tokens(user)

        payload = {
            "first_name": user_data["name"],
            "last_name": "",
            "upload_avatar": user_data["avatar_url"],
        }
        new_user = user_services.svc_create_user(payload, db)

        return user_services.gen_user_info_and_tokens(new_user)

    except Exception as e:
        get_social_login_exception(e)
