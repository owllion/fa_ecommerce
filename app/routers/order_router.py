from fastapi import Depends, HTTPException, status

from ..constants import api_msgs
from ..exceptions.custom_http_exception import CustomHTTPException
from ..schemas import order_schema
from ..services import order_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'order',
    plural_prefix = 'orders',
    tags = ['order']
)

@protected_singular.post(
    "/", 
    **get_path_decorator_settings(
        description= "Successfully create the order."
    )
)
async def create_order(
    req: Request,
    payload: order_schema.OrderCreateSchema, 
    db: Session = Depends(db.get_db)
):
    
    try:
        order_id = await order_services.create_order_and_return_id(payload, db)

        await order_services.create_order_item(payload.order_items,order_id,db)

        if payload.discount_code:
            order_services.set_coupon_as_used(req, payload.discount_code, db)

        await order_services.update_stock_and_sales_for_all_order_items(payload.order_items, db)
        

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.get(
    "/{order_id}",
    **get_path_decorator_settings(
        description= "Get the data of a order",
        response_model= order_schema.OrderSchema
    )
)
def get_order(order_id: str,db:Session = Depends(db.get_db)):
    try:
       order = order_services.get_order_or_raise_not_found(order_id, db)
       return order
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_plural.get(
    "/",
    **get_path_decorator_settings(
        description= "Get the order list",
        response_model= list[order_schema.OrderSchema]
    )
)
async def get_orders(db:Session = Depends(db.get_db)):
    try:
        orders = await order_services.get_all_orders(db)
        return orders
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
    

@protected_plural.get(
    "/user/{user_id}",
    **get_path_decorator_settings(
        description= "Get the specific user's order list",
        response_model= list[order_schema.OrderSchema]
    )
)
async def get_user_orders(
    user_id: str,
    db:Session = Depends(db.get_db)
):
    try:
        orders = await order_services.get_orders_by_user_id(user_id,db)

        return orders
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description= "Successfully update the order.",
    )
)
async def update_order(
    payload: order_schema.OrderUpdateSchema,
    db:Session = Depends(db.get_db)
):
    try:
        order = await order_services.get_order_or_raise_not_found(payload.id, db)
        
        await order_services.update_order_record(payload, order, db)
        
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


@protected_singular.delete(
    "/{order_id}",
    **get_path_decorator_settings(
        description= "Successfully delete the order.",
    )
)
async def delete_order(order_id: str,db:Session = Depends(db.get_db)):
    try:
        await order_services.delete_order_record(order_id, db)
        
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


