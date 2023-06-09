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
from sqlalchemy.orm import Session

from ...database import db
from ...exceptions.main import get_exception
from ...models.cart import cart_item_model
from ...schemas import cart_schema, common_schema, product_schema, user_schema
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
            db.commit()
            operation_msg = "remove from fav"

        else:
            product_services.add_to_fav(user, product)
            operation_msg = "add to fav"

        db.commit()
        return {"msg": operation_msg}

    except Exception as e:
        get_exception(e)


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
        get_exception(e)
