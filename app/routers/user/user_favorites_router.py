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
from ...schemas import cart_schema, common_schema, product_schema, user_schema
from ...schemas.user_schema import SupportedField, VerifiedValue
from ...services import product_services, user_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="user-favorite", plural_prefix="user-favorites", tags=["user-favorite"]
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
        description="Add or remove a product to/from user's list of favorites"
    )
)
def toggle_fav(
    req: Request, payload: product_schema.ToggleFavoriteSchema, db: Session = Depends(db.get_db)
):
    try:
        user = req.state.mydata

        product = product_services.get_product_or_raise_not_found(payload.product_id, db)

        if product_services.product_in_user_fav(user.id, payload.product_id, db):
            product_services.remove_from_fav(user, product)
        else:
            product_services.add_to_fav(user, product)

        db.commit()

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_plural.get(
    "/",
    **get_path_decorator_settings(
        description="get user's fav list",
        response_model=list[common_schema.ProductInfoInCartSchema],
    )
)
def get_user_favs(req: Request, db: Session = Depends(db.get_db)):
    try:
        return req.state.mydata.favorites
    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))
