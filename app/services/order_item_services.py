from fastapi import Depends, status
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..exceptions.get_exception import raise_http_exception
from ..models.order import order_item_model
from ..schemas import order_schema


async def create_order_item(payload: order_schema.OrderItemCreateSchema,db: Session):

    order_item = order_item_model.OrderItem(**payload.dict())
    
    db.add(order_item)
    db.commit()


def find_order_item(
    order_id: str,
    product_id: str,
    size: str,
    db: Session
):
    order_item = db\
        .query(order_item_model.OrderItem)\
        .filter(
            order_item_model.OrderItem.product_id == product_id,
            order_item_model.OrderItem.order_id == order_id,
            order_item_model.OrderItem.size == size
        )\
        .first()

    return order_item
        

def order_item_exists(
    order_id: str,
    product_id: str,
    size: str,
    db: Session
):
    order_item = find_order_item(order_id,product_id, size,db)
    if order_item: return True 

    raise_http_exception(api_msgs.ORDER_ITEM_NOT_FOUND)

def get_order_item_or_raise_not_found(
    order_id: str,
    product_id: str,
    size: str,
    db: Session
):
    order_item = find_order_item(order_id,product_id,size,db)
    if order_item: return order_item

    raise_http_exception(api_msgs.ORDER_ITEM_NOT_FOUND)

def delete_order_item_record(
    order_item: order_item_model.OrderItem,
    db: Session
):
    db.delete(order_item)
    db.commit()
