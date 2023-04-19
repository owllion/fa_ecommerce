from fastapi import Depends, status
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..exceptions.get_exception import raise_http_exception
from ..models.order import order_item_model
from ..schemas import order_schema


async def create_order_item(payload: order_schema.OrderItemCreateSchema,db: Session):
    print(payload,'this is payload in c_o_i')

    order_item = order_item_model.OrderItem(**payload.dict())
    print(order_item,'this is order_item')
    
    db.add(order_item)
    db.commit()


async def find_order_item(
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
        

async def order_item_not_exists(
    order_id: str,
    product_id: str,
    size: str,
    db: Session
):
    order_item = find_order_item(order_id,product_id, size,db)
    if not order_item: return True 

    raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.ORDER_ITEM_NOT_FOUND
    )

async def get_order_item_or_raise_not_found(
    order_id: str,
    product_id: str,
    size: str,
    db: Session
):
    order_item = find_order_item(order_id,product_id,size,db)
    if order_item: return order_item

    raise_http_exception(
        status.HTTP_400_BAD_REQUEST,
        api_msgs.ORDER_ITEM_NOT_FOUND
    )

async def delete_order_item_record(
    order_id: str,
    product_id: str,
    size: str,
    db: Session
):
    order_item = get_order_item_or_raise_not_found(order_id,product_id,size,db)

    db.delete(order_item)
    db.commit()
