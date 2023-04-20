from fastapi import Depends, Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..constants import api_msgs
from ..database import db
from ..exceptions.get_exception import raise_http_exception
from ..models.order import order_item_model, order_model
from ..models.product import product_item_model, product_model, size_model
from ..schemas import order_schema, product_item_schema
from . import coupon_services, product_item_services, product_services


def find_corresponding_size_id_with(size: str, db: Session):
    return db.query(size_model.Size).filter_by(value= size).first().id


def update_stock_and_sales(item: order_schema.OrderItemSchema, db: Session):
    item.size = item.size.value
    size_id = find_corresponding_size_id_with(item.size, db)

    product_item = product_item_services.get_product_item_or_raise_not_found(item.product_id, size_id, db)
    # print(product_item.stock,'這是stock')
    # print(product_item.sales,'這是sales')
    product_item.stock -= item.qty
    product_item.sales += item.qty

    db.commit()


def update_stock_and_sales_for_all_order_items(order_items: list[order_schema.OrderItemSchema], db: Session):
    for item in order_items:
        update_stock_and_sales(item, db)


def create_order_and_return_id(payload: order_schema.OrderCreateSchema,db: Session):

    payload.payment_status = payload.payment_status.value
    payload.order_status = payload.order_status.value

    order_data = {k: v for k, v in payload.dict().items() if k != 'order_items'}
    print(order_data)

    order = order_model.Order(**order_data)

    db.add(order)
    db.commit()
    db.refresh(order)  #從資料庫中重新加載對象

    return order.id

def find_order_with_id(id: str, db: Session):
    order = db.query(order_model.Order).filter_by(id=id).first()
    return order

def order_exists(order_id: str, db: Session):
    order = find_order_with_id(order_id, db)
    if order: return True

    raise_http_exception(
        api_msgs.ORDER_NOT_FOUND
    )

def get_order_or_raise_not_found(id: str, db: Session):
    order = find_order_with_id(id, db)
    if not order:
        raise_http_exception(api_msgs.ORDER_NOT_FOUND)
    
    return order

def get_all_orders(db: Session):
    return db.query(order_model.Order).all()

def get_orders_by_user_id(user_id: str, db: Session):
    return db.query(order_model.Order).filter_by(owner_id=user_id).all()


def update_order_record(
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

def delete_order_record(order_id: str, db: Session):
    order = get_order_or_raise_not_found(order_id, db)
    db.delete(order)
    db.commit()

def create_order_item(
    order_items: list[order_schema.OrderItemCreateSchema],
    order_id: str,
    db: Session
):
    order_items = [jsonable_encoder(item) for item in order_items]

    for item in order_items:

        item['order_id'] = order_id

        order_item = order_item_model.OrderItem(**item)

        db.add(order_item)
        db.commit() 
        db.refresh(order_item) 
         
def set_coupon_as_used(req: Request, code: str, db: Session):
    coupon = coupon_services.get_coupon_or_raise_not_found(req, code, db)

    coupon.is_used = True

    db.commit()
