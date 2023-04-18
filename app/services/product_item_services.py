from fastapi import Depends, status
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..database import db
from ..exceptions.get_exception import raise_http_exception
from ..models.product import product_item_model, product_model, size_model
from ..schemas import product_item_schema
from . import product_services

#general-----

def save_to_db(item: product_item_schema.ProductItemSchema,db: Session):
    db.add(item)
    db.commit()

#general-----


#---product_item---

def create_product_item(payload: product_item_schema.ProductItemCreateSchema):
    product_item = product_item_model.ProductItem(
        product_id = payload.product_id,
        size_id = payload.size_id,
        stock = payload.stock,
        sales = payload.sales
    )
    return product_item

def update_item(
    payload: product_item_schema.ProductItemUpdateSchema, 
    product_item: product_item_model.ProductItem,
    db: Session
):
    data = payload.dict(exclude_unset=True)

    for field,value in data.items():
        if hasattr(product_item, field):
            setattr(product_item, field, value)
    
    db.commit()


def find_product_item(
    product_id: str,
    size_id: str,
    db: Session
):
    product_item = db\
        .query(product_item_model.ProductItem)\
        .filter(
            product_item_model.ProductItem.size_id == size_id,
            product_item_model.ProductItem.product_id == product_id

        )\
        .first()

    return product_item
        

def product_item_not_exists(product_id: str,size_id: str,
db: Session):
    product_item = find_product_item(product_id,size_id,db)
    if not product_item: return True 

    raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.PRODUCT_ITEM_ALREADY_EXISTS
    )

def get_product_item_or_raise_not_found(product_id: str,size_id: str,
db: Session):
    product_item = find_product_item(product_id,size_id,db)
    if product_item: return True 

    raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.PRODUCT_ITEM_NOT_FOUND
    )

#---product_item---


#---product---
def get_product(product_id: str, db: Session):
    product = product_services.find_product_with_id(product_id,db)
    
    return product

def product_exists(product_id: int, db: Session):
    product = get_product(product_id, db)
    if product: return True

    raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.PRODUCT_NOT_FOUND
    )
 

#---product---

       
#---size---
def get_size(size_id: str, db: Session):
    size = db\
            .query(size_model.Size)\
            .filter(size_model.Size.id == size_id)\
            .first()
    
    return size

def size_exists(size_id: str, db: Session):
    size = get_size(size_id, db)
    if size: return True

    raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.SIZE_NOT_FOUND
    )

#---size---

