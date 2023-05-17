import json
import os
from datetime import timedelta
from enum import Enum
from typing import Annotated

import requests
from authlib.integrations.starlette_client import OAuthError
from decouple import config
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.custom_http_exception import CustomHTTPException
from ...exceptions.main import raise_http_exception
from ...schemas import auth_schema, user_schema
from ...services import user_services
from ...utils.common.logger import logger
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import get_path_decorator_settings
from ...utils.security import security

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("test-get")
async def test_get(req: Request):
    client = req.app.state.redis
    data = {
        "product_name": "develop prepare nothing",
        "description": "Skin population play hold check writer behavior. Drug if whole science wall accept many. Simple three forget go south image.",
        "thumbnail": "https://placekitten.com/320/400",
        "price": 421,
        "brand": "Cartier",
        "category": "hat",
        "color": "LightPink",
        "id": "06d053b91f174625952b3c63ff7d5a28",
        "created_at": "2023-04-12T16:48:15",
        "updated_at": "2023-04-12T16:48:15",
        "reviews": [],
        "images": [
            {"url": "https://picsum.photos/720/900"},
            {"url": "https://picsum.photos/720/900"},
            {"url": "https://placekitten.com/720/900"},
        ],
        "thumbnails": [
            {"url": "https://picsum.photos/320/400"},
            {"url": "https://dummyimage.com/320x400"},
            {"url": "https://dummyimage.com/320x400"},
        ],
    }
    # await client.setex("test1", timedelta(seconds=30), json.dumps(data))
    test_obj = {"name": "ruel", "age": 123}
    # await client.set(json.dumps(test_obj), "測試值")

    # ----
    rr = await client.get(json.dumps(test_obj))
    # 規律的話...searchOptions
    # 用hash好了
    print(rr, "這是123rrr，左邊應該要是'測試值'")
    res = await client.get("test1")
    if res:
        print(res, "這是ressss")
        res = json.loads(res)
        print(res["product_name"])
        print(res["thumbnails"][0])
    else:
        print("過期了")

    db_name = config("DB_NAME")
    return db_name


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    # response_model=user_schema.RegisterResultSchema,
)
async def create_user(payload: user_schema.UserCreateSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Account already exist"
            )

        new_user = user_services.create_user_service(payload, db)

        link_params = {
            "user_id": new_user.id,
            "user_email": new_user.email,
            "link_type": "verify",
            "url_params": "verify-email",
        }

        await user_services.send_verify_or_reset_link(link_params)

        return_data = jsonable_encoder(new_user, by_alias=False)
        # 改成易於serilize的格式(dict)

        # return_data.pop('password')

        print(return_data, "這是return data")

        # return_data['token'] = security.create_token(new_user.id,'access')
        # return_data['refresh_token'] = security.create_token(new_user.id,'refresh')

        # 註冊後根本不用船任何東西，因為沒認證email仕進不去的
        # return {
        #     'token': security.create_token(new_user.id,'access'),
        #     'refresh_token': security.create_token(new_user.id,'refresh'),
        #     'user': return_data,
        # }

    except Exception as e:
        logger.error(e, exc_info=True)

        if type(e).__name__ == "HTTPException":
            raise e
        raise CustomHTTPException(detail=str(e))


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=user_schema.LoginResultSchema
)
def login(payload: user_schema.LoginUserSchema, db: Session = Depends(db.get_db)):
    try:
        user = user_services.find_user_with_email(payload.email, db)

        if not user:
            raise_http_exception(api_msgs.USER_NOT_FOUND)

        if user_services.password_is_matched(
            payload.password, user.password
        ) and user_services.user_is_verified(user.verified):
            # cart_length = db.query()
            return {
                "token": security.create_token(user.id, "access"),
                "refresh_token": security.create_token(user.id, "refresh"),
                "user": user,
                "cart_length": len(user.cart.cart_items),
            }

    except Exception as e:
        logger.error(e, exc_info=True)
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@router.post("/refresh-token", response_model=user_schema.AccessAndRefreshTokenSchema)
def get_refresh_token(payload: user_schema.TokenSchema, db: Session = Depends(db.get_db)):
    try:
        decoded_data = security.decode_token(payload.token, "refresh", db)

        return {
            "token": security.create_token(decoded_data.id, "access"),
            "refresh_token": security.create_token(decoded_data.id, "refresh"),
        }

    except Exception as e:
        logger.error(e, exc_info=True)
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@router.post(
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
        logger.error(e, exc_info=True)
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))
