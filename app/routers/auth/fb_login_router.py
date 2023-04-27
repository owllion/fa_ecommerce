import json
import os
from enum import Enum
from typing import Annotated

import requests
from authlib.integrations.starlette_client import OAuthError
from decouple import config
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.custom_http_exception import CustomHTTPException
from ...exceptions.get_exception import raise_http_exception
from ...schemas import auth_schema, user_schema
from ...services import user_services
from ...utils import security
from ...utils.dependencies import *
from ...utils.logger import logger
from ...utils.router_settings import get_path_decorator_settings
from .auth_router import router

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


client_id = config("FB_CLIENT_ID")
client_secret = config("FB_CLIENT_SECRET")

authorization_base_url = 'https://www.facebook.com/v16.0/dialog/oauth'
token_url = 'https://graph.facebook.com/v16.0/oauth/access_token'
# redirect_uri ='https://localhost:3000/auth/fb-login/callback'
redirect_uri ='https://localhost:3000/auth/fb-login/callback'





facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
facebook = facebook_compliance_fix(facebook)
scope = ["public_profile", "email"]

@router.get('/fb-login')
async def fb_login():
    url,state = facebook.authorization_url(authorization_base_url)
    print(url,'這是臉書url')
    return {"url": url}

@router.post('/fb-auth')
async def fb_auth(
    payload: auth_schema.SocialLoginSchema,
    db: Session = Depends(db.get_db)
):
    try:
        facebook.fetch_token(
            token_url, 
            client_secret=client_secret,
            authorization_response= payload.reqUrl
        )

        res = facebook.get('https://graph.facebook.com/me?')

        print(res.content,'this is r.content')

        user_data = json.loads(res.text)

        print(user_data,'這是userdata')
        # print(user_data.email,'這是email .')
        print(user_data['email'],'這是email []')
        
        #建一個 fb_username 欄位(拿login值)
        
        #建立新的user
        # found_user = user_services.find_user_with_email(user_data['email'],db)

        # if found_user:
        #     raise_http_exception(api_msgs.USER_ALREADY_EXISTS)
        
        # payload = {
        #     'email' : user_data['email'],
        #     'first_name': user_data['given_name'],
        #     'last_name': user_data['family_name'] if 'family_name' in user_data else '',
        #     'upload_avatar': user_data['picture']
        # }

        # new_user = user_services.create_user_service(payload, db)
    
        # return {
        #     'token': security.create_token(new_user.id,'access'),
        #     'refresh_token': security.create_token(new_user.id,'refresh'),
        #     'user': new_user,
        # }
        return {"msg": '臉書成功登入喔'}

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        if isinstance(e, (OAuthError,)):
            raise_http_exception(
            detail= e.description,
            status_code= status.HTTP_401_UNAUTHORIZED
        )
        raise_http_exception(
            api_msgs.SERVER_ERROR
        )