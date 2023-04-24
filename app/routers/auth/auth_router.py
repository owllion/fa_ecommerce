from enum import Enum
from typing import Annotated

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

# from starlette.requests import Request
from starlette.config import Config

from ...database import db
from ...exceptions.custom_http_exception import CustomHTTPException
from ...schemas import user_schema
from ...services import user_services
from ...utils import security
from ...utils.dependencies import *
from ...utils.logger import logger
from ...utils.router_settings import get_path_decorator_settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
 
config = Config('...env')
oauth = OAuth(config)

#Authlib will fetch this server_metadata_url to configure the OAuth client for you
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)



@router.get(
    "/google-login", 
    description=" redirect user to Google account website.When you grant access from Google website, Google will redirect back to your given redirect_uri, which is request.url_for('auth')."
)
async def google_login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth(request: Request):
    try:
        #get the authrization code or related data from the req
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')

        if user:
            request.session['user'] = dict(user)

        return RedirectResponse(url='/')
    
    except OAuthError as e:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= e.error
        )


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
#------------------


@router.post(
    '/register', 
    status_code= status.HTTP_201_CREATED,
    response_model= user_schema.RegisterResultSchema 
)
async def create_user(
    payload: user_schema.UserCreateSchema, 
    db: Session = Depends(db.get_db)
):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,detail='Account already exist'
            )

        new_user = user_services.save_data_then_return(payload,db)

        link_params = {
            'user_id': new_user.id,
            'user_email': new_user.email,
            'link_type' : 'verify',
            'url_params' : 'verify-email'   
        }
        
        await user_services.send_verify_or_reset_link(link_params)

        return_data = jsonable_encoder(new_user, by_alias=False)
        #改成易於serilize的格式(dict)

        # return_data.pop('password')

        print(return_data,'這是return data') 

        # return_data['token'] = security.create_token(new_user.id,'access')
        # return_data['refresh_token'] = security.create_token(new_user.id,'refresh')


        return {
            'token': security.create_token(new_user.id,'access'),
            'refresh_token': security.create_token(new_user.id,'refresh'),
            'user': return_data,
        }

    except Exception as e:
        logger.error(e, exc_info=True)

        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))



@router.post(
    '/login',
    status_code= status.HTTP_200_OK,
    response_model= user_schema.LoginResultSchema
)
def login(
    payload: user_schema.LoginUserSchema, 
    db: Session = Depends(db.get_db)
):
    try:
        user = user_services.find_user_with_email(payload.email, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User does not exist!'
            )


        if user_services.password_is_matched(payload.password, user.password) and user_services.user_is_verified(user.verified):
            # cart_length = db.query()
            return { 
                'token': security.create_token(user.id,"access"),
                'refresh_token': security.create_token(user.id,"refresh"),
                'user': user,
                'cart_length': 2      
            }


    except HTTPException as e:
        logger.error(e, exc_info=True)
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))


    


@router.post(
    '/refresh-token', response_model=user_schema.AccessAndRefreshTokenSchema
)
def get_refresh_token(
    payload: user_schema.TokenSchema,
    db: Session = Depends(db.get_db)
):
    try:
        decoded_data = security.decode_token(payload.token,'refresh',db)

        return {
            'token': security.create_token(
                decoded_data.id,
                'access'
            ),
            'refresh_token': security.create_token(
                decoded_data.id,
                'refresh'
            )
        }

    except Exception as e:
        logger.error(e, exc_info=True)
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))


@router.post(
    "/verify-email-token", 
    **get_path_decorator_settings(
        response_model= user_schema.RegisterResultSchema,
        description="Verify user email with the token extracted from the link provided in the email. Returns a success message if the token is valid."
    )
)
def verify_token_from_email_link(
    payload: user_schema.TokenSchema,
    db: Session = Depends(db.get_db)
):
    try:
        decoded_data = security.decode_token(payload.token,'access',db)
        decoded_data.verified = 1
        db.commit()

        return {
            'token': security.create_token(
                decoded_data.id,
                'access'
            ),
            'refresh_token': security.create_token(
                decoded_data.id,
                'refresh'
            ),
            'user': decoded_data,
        }

    except Exception as e:
        if type(e).__name__ == 'HTTPException': raise e
        raise CustomHTTPException(detail= str(e))