import json

import requests
from authlib.integrations.starlette_client import OAuthError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.custom_http_exception import CustomHTTPException
from ...exceptions.get_exception import raise_http_exception
from ...services import user_services
from ...utils import security
from .auth_router import router


@router.get('/google-login')
async def google_auth(
    access_token: str,
    db: Session = Depends(db.get_db)
):
    try:
        res = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}")

        user_data = json.loads(res.text)

        print(user_data,'這是userdata')
        # print(user_data.email,'這是email .')
        print(user_data['email'],'這是email []')
        
        #建立新的user
        found_user = user_services.find_user_with_email(user_data['email'],db)

        if found_user:
            raise_http_exception(api_msgs.USER_ALREADY_EXISTS)
        
        payload = {
            'email' : user_data['email'],
            'first_name': user_data['given_name'],
            'last_name': user_data['family_name'] if 'family_name' in user_data else '',
            'upload_avatar': user_data['picture']
        }

        new_user = user_services.create_user_service(payload, db)
    
        return {
            'token': security.create_token(new_user.id,'access'),
            'refresh_token': security.create_token(new_user.id,'refresh'),
            'user': new_user,
        }

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        if isinstance(e, (OAuthError,)):
            raise_http_exception(
            detail= e.description,
            status_code= status.HTTP_401_UNAUTHORIZED
        )
        raise CustomHTTPException(detail= str(e))
    
