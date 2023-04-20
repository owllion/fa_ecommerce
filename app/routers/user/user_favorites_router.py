from enum import Enum
from typing import Annotated, Generic, TypeVar

from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ...constants import api_msgs
from ...database import db
from ...exceptions.custom_http_exception import CustomHTTPException
from ...models.cart import cart_item_model
from ...schemas import cart_schema, product_schema, user_schema
from ...schemas.user_schema import SupportedField, VerifiedValue
from ...services import product_services, user_services
from ...utils.dependencies import *
from ...utils.logger import logger
from ...utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'user-favorite',
    plural_prefix = 'user-favorites',
    tags = ['user-favorite']
)