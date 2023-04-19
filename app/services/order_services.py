from fastapi import Depends, status
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..database import db
from ..exceptions.get_exception import raise_http_exception
from ..models.order import order_item_model, order_model
from ..models.product import product_item_model, product_model, size_model
from ..schemas import order_schema, product_item_schema
from . import product_item_services, product_services


def find_corresponding_size_id_with(size: str, db: Session):
    return db.query(size_model.Size).filter_by(value= size).first().id


async def update_stock_and_sales(item: order_schema.OrderItemSchema, db: Session):
    item.size = item.size.value
    size_id = find_corresponding_size_id_with(item.size, db)

    product_item = product_item_services.get_product_item_or_raise_not_found(item.product_id, size_id, db)
    # print(product_item.stock,'這是stock')
    # print(product_item.sales,'這是sales')
    product_item.stock -= item.qty
    product_item.sales += item.qty

    db.commit()


async def update_stock_and_sales_for_all_order_items(order_items: list[order_schema.OrderItemSchema], db: Session):
    for item in order_items:
        await update_stock_and_sales(item, db)


async def create_order(payload: order_schema.OrderCreateSchema,db: Session):

    payload.payment_status = payload.payment_status.value
    payload.order_status = payload.order_status.value

    order_data = {k: v for k, v in payload.dict().items() if k != 'order_items'}
    print(order_data)

    order = order_model.Order(**order_data)

    db.add(order)
    db.commit()
    db.refresh(order)  #從資料庫中重新加載對象

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
    if payload.order_status:
        payload.order_status = payload.order_status.value
    
    data = payload.dict(exclude_unset=True)
    
    for field,value in data.items():
        if hasattr(order, field):
            setattr(order, field, value)
    
    db.commit()

async def delete_order_record(order_id: str, db: Session):
    order = await get_order_or_raise_not_found(order_id, db)
    db.delete(order)
    db.commit()

async def create_order_item(
    order_items: list[order_schema.OrderItemCreateSchema],
    db: Session
):
    for item in order_items:
        order_item = order_item_model.OrderItem(**item.dict())

        db.add(order_item)
        db.commit() 
        db.refresh(order_item)     
