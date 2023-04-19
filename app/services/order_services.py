from fastapi import Depends, status
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..database import db
from ..exceptions.get_exception import raise_http_exception
from ..models.order import order_item_model, order_model
from ..models.product import product_item_model, product_model, size_model
from ..schemas import order_schema, product_item_schema
from . import product_services

#general-----

def save_to_db(item: product_item_schema.ProductItemSchema,db: Session):
    db.add(item)
    db.commit()

def delete_item(item: product_item_schema.ProductItemSchema,db: Session):
    db.delete(item)
    db.commit()

#general-----
#----------order
async def create_order(payload: order_schema.OrderCreateSchema,db: Session):
    order_data = {k: v for k, v in payload.dict().items() if k != 'order_items'}
    order = order_model.Order(**order_data)
    # order = order_model.Order(**payload.dict())
    db.add(order)
    db.commit()
    db.refresh(order)  # 從資料庫中重新加載對象
    print("cdreate order最後")

async def find_order_with_id(id: str, db: Session):
    order = db.query(order_model.Order).filter_by(id=id).first()
    return order

async def order_exists(order_id: str, db: Session):
    order = find_order_with_id(order_id, db)
    if order: return True
    raise raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.ORDER_NOT_FOUND
    )

async def get_order_or_raise_not_found(id: str, db: Session):
    order = await find_order_with_id(id, db)
    if not order:
        raise raise_http_exception(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= api_msgs.ORDER_NOT_FOUND
        )
    
    return order

async def get_all_orders(db: Session):
    return db.query(order_model.Order).all()

async def get_orders_by_user_id(user_id: str, db: Session):
    return db.query(order_model.Order).filter_by(owner_id=user_id).all()


async def update_order_record(
    payload: order_schema.OrderUpdateSchema, 
    order: order_model.Order,
    db: Session
):
    data = payload.dict(exclude_unset=True)

    for field,value in data.items():
        if hasattr(order, field):
            setattr(order, field, value)
    
    db.commit()

async def delete_order_record(order_id: str, db: Session):
    order = await get_order_or_raise_not_found(order_id, db)
    db.delete(order)
    db.commit()


#----------order---

#------order_item----
async def create_order_item(
    order_items: list[order_schema.OrderItemCreateSchema],
    db: Session
):
    print(order_items,'這是新增 order_item')

    for item in order_items:
        order_item = order_item_model.OrderItem(**item.dict())
        print(order_item,'this is order_item')
        db.add(order_item)
        # db.refresh(order_item)
       
    db.commit()
    print(order_items,'這是commit order_item')
     

#------order_item----



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
    if product_item: return product_item

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

