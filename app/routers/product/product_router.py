import json
from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi import exceptions as es
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, asc, desc, func

from ...constants import api_msgs
from ...exceptions.main import get_exception, raise_http_exception
from ...models.product import product_item_model, product_model
from ...schemas import product_item_schema, product_schema
from ...services import product_services
from ...utils.depends.dependencies import *
from ...utils.redis.keys import (
    best_selling_products_key,
    number_of_search_result_key,
    products_key,
    search_options_key,
)
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="product", plural_prefix="products", tags=["product"]
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
        description="Successfully create product.", response_model=product_schema.ProductSchema
    )
)
def create_product(payload: product_schema.ProductCreateSchema, db: Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_name(payload.product_name, db)

        if product:
            raise_http_exception(api_msgs.PRODUCT_ALREADY_EXISTS)

        new_product = product_services.svc_create_product(payload, db)

        return new_product

    except Exception as e:
        get_exception(e)


@public_singular.get(
    "/{product_id}",
    **get_path_decorator_settings(
        description="Get the data of a single product.",
        response_model=product_schema.SingleProductSchema,
    )
)
def get_product(req: Request, product_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis

        cached_product = client.json().get(products_key(product_id), ".")

        if cached_product:
            return json.loads(cached_product)

        product = product_services.get_populated_product_or_raise_not_found(product_id, db)

        if not product:
            raise_http_exception(api_msgs.PRODUCT_NOT_FOUND)

        client.json().set(products_key(product_id), ".", json.dumps(jsonable_encoder(product)))

        client.expire(products_key(product_id), timedelta(seconds=20))

        return product

    except Exception as e:
        get_exception(e)


@public_plural.post(
    "/",
    **get_path_decorator_settings(
        description="Get the product list",
        response_model=product_schema.ResponsePaginateProductsSchema,
    )
)
def get_products(payload: product_schema.PaginateProductsSchema, db: Session = Depends(db.get_db)):
    try:
        query = db.query(product_model.Product)

        total, filtered_list = product_services.filter_products(query, payload).values()

        return {"list": filtered_list or [], "total": total or 0}

    except Exception as e:
        get_exception(e)


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description="Successfully update the product.",
    )
)
def update_product(payload: product_schema.ProductUpdateSchema, db: Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(payload.id, db)

        if not product:
            raise_http_exception(api_msgs.PRODUCT_NOT_FOUND)

        data = payload.dict(exclude_unset=True)

        for field, value in data.items():
            if hasattr(product, field):
                setattr(product, field, value)

        db.commit()

    except Exception as e:
        get_exception(e)


@protected_singular.delete(
    "/{product_id}",
    **get_path_decorator_settings(
        description="Successfully delete the product.",
    )
)
def delete_product(product_id: str, db: Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(product_id, db)

        if not product:
            raise_http_exception(api_msgs.PRODUCT_NOT_FOUND)

        db.delete(product)
        db.commit()

    except Exception as e:
        get_exception(e)


@public_plural.get(
    "/best-seller",
    **get_path_decorator_settings(
        description="Successfully obtained a list of the top-selling products.",
        response_model=list[product_item_schema.BestSellerProductSchema],
    )
)
def get_top_selling_products(req: Request, db: Session = Depends(db.get_db)):
    try:
        product_items = (
            db.query(product_item_model.ProductItem)
            .order_by(desc(getattr(product_item_model.ProductItem, "sales")))
            .limit(10)
            .all()
        )

        dict_products = list(map(lambda x: jsonable_encoder(x.parent_product), product_items))

        return dict_products

    except Exception as e:
        get_exception(e)
