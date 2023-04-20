from fastapi import APIRouter, Depends, HTTPException
from fastapi import exceptions as es
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func

from ...constants import api_msgs, exceptions
from ...exceptions.custom_http_exception import CustomHTTPException
from ...models.product import product_item_model, product_model, size_model
from ...schemas import product_item_schema
from ...services import product_item_services, product_services
from ...utils.dependencies import *
from ...utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'product-item',
    plural_prefix = 'product-items',
    tags = ['product-item']
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
    description= "create a product item",
    response_model= product_item_schema.ProductItemSchema
    )
)
def create_product_item(
    payload: product_item_schema.ProductItemCreateSchema,
    db: Session = Depends(db.get_db)
):
    try:
        if\
            product_item_services.product_exists(payload.product_id, db)\
                and\
            product_item_services.size_exists(payload.size_id, db):
            if product_item_services.product_item_not_exists:
                product_item = product_item_services.create_product_item(payload)

                product_item_services.save_to_db(product_item,db)

                return product_item

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(
            detail= str(e)
        )

@protected_singular.delete(
    "/",
    **get_path_decorator_settings(
    description= "delete a product item"
    )
)
def delete_product_item(
    payload: product_item_schema.ProductItemDeleteSchema,
    db: Session = Depends(db.get_db)
):
    try:
        if\
            product_item_services.product_exists(payload.product_id, db)\
                and\
             product_item_services.size_exists(payload.size_id, db):

                product_item = product_item_services.get_product_item_or_raise_not_found(payload.product_id, payload.size_id, db)

                product_item_services.delete_item(product_item, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(
            detail= str(e)
        )

@protected_singular.put(
    "/",
    **get_path_decorator_settings(
    description= "update a product item"
    )
)
def update_product_item(
    payload: product_item_schema.ProductItemUpdateSchema,
    db: Session = Depends(db.get_db)
):
    try:
        if\
            product_item_services.product_exists(payload.product_id, db)\
                and\
            product_item_services.size_exists(payload.size_id, db):
             
                product_item = product_item_services.get_product_item_or_raise_not_found(payload.product_id, payload.size_id, db)
            
                product_item_services.update_item(payload, product_item, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(
            detail= str(e)
        )
    
@public_plural.get(
    "/all",
    **get_path_decorator_settings(
    description= "get the product item list",
    response_model= list[product_item_schema.ProductItemSchema]
    )
)
def get_all_product_items(db: Session = Depends(db.get_db)):
    items = db.query(product_item_model.ProductItem).all()
    return items


@public_plural.get(
    "/product/{product_id}",
    **get_path_decorator_settings(
        description= "get all the product items of specified product.",
        response_model= list[product_item_schema.ProductItemSchema]
    )
)
def get_product_items(
    product_id: str,
    db: Session = Depends(db.get_db)
):
    items = db\
        .query(product_item_model.ProductItem)\
        .filter(product_item_model.ProductItem.product_id == product_id)\
        .all()

    return items





















