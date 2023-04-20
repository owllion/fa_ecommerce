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

@protected_singular.post(
    "/",
    **get_path_decorator_settings(
        description= "Add or remove a product to/from user's list of favorites"
    )
)
def toggle_fav(
    req: Request,
    payload: product_schema.ToggleFavoriteSchema,
    db: Session = Depends(db.get_db)
):
    try:
        user = req.state.mydata

        product = product_services.get_product_or_raise_not_found(payload.product_id,db)

        if product_services.product_in_user_fav(user, payload.product_id, db):
            user.favorites.remove(product)
        else:
            user.favorites.append(product)
        
        db.commit()
        

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
    
# @protected_singular(
#     **get_path_decorator_settings(
#         description= "Remove the product from user's fav list"
#     )
# )
# def remove_from_fav(req: Request,product_id: str, db: Session = Depends(db.get_db)):
#     try:
#         user = req.state.mydata

#         product = product_services.get_product_or_raise_not_found(product_id, db)

#         user.favorites.remove(product)

#         db.commit()
        

#     except Exception as e:
#         if isinstance(e, (HTTPException,)): raise e
#         raise CustomHTTPException(detail= str(e))