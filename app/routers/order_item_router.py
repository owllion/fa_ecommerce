from fastapi import Depends, HTTPException, status

from ..constants import api_msgs
from ..exceptions.custom_http_exception import CustomHTTPException
from ..schemas import order_schema
from ..services import order_item_services, order_services,product_item_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'order_item',
    plural_prefix = 'order_items',
    tags = ['order_item']
)

@protected_singular.post(
    "/", 
    **get_path_decorator_settings(
        description= "Successfully create the order_item.",
        response_model= order_schema.OrderItemSchema
    )
)
async def create_order(
    payload: order_schema.OrderItemCreateSchema, 
    db: Session = Depends(db.get_db)
):
    
    try:
        await order_item_services.create_order_item(payload, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


# @protected_singular.get(
#     "/{order_id}",
#     **get_path_decorator_settings(
#         description= "Get the data of a orde_item",
#         response_model= order_schema.OrderSchema
#     )
# )
# def get_order(order_id: str,db:Session = Depends(db.get_db)):
#     try:
#        order = order_services.get_order_or_raise_not_found(order_id, db)
#        return order
          
#     except Exception as e:
#         if isinstance(e, (HTTPException,)): raise e
#         raise CustomHTTPException(detail= str(e))


@protected_plural.get(
    "/",
    **get_path_decorator_settings(
        description= "Get the order_item list",
        response_model= list[order_schema.OrderItemSchema]
    )
)
async def get_all_order_items(db:Session = Depends(db.get_db)):
    try:
        orders = await order_item_services.get_all_items(db)
        return orders
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
    

@protected_plural.get(
    "/{order_id}",
    **get_path_decorator_settings(
        description= "Get the specific order's order items",
        response_model= list[order_schema.OrderItemSchema]
    )
)
async def get_order_items(
    order_id: str,
    db:Session = Depends(db.get_db)
):
    try:
       order = order_services.get_order_or_raise_not_found(order_id, db)
        return order.order_items
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


# @protected_singular.put(
#     "/",
#     **get_path_decorator_settings(
#         description= "Successfully update the order item.",
#     )
# )
# async def update_order(
#     payload: order_schema.OrderItemUpdateSchema,
#     db:Session = Depends(db.get_db)
# ):
#     try:
#         order = await order_services.get_order_or_raise_not_found(payload.id, db)
        
#         order_services.update_order_record(payload, order, db)
        
#     except Exception as e:
#         if isinstance(e, (HTTPException,)): raise e
#         raise CustomHTTPException(detail= str(e))


@protected_singular.delete(
    "/",
    **get_path_decorator_settings(
        description= "Successfully delete the order item.",
    )
)
async def delete_order_item(
    payload: order_schema.OrderItemDeleteSchema,
    db:Session = Depends(db.get_db)
):    
    product_id,order_id,size = payload

    try:
        if\
            product_item_services.product_exists(product_id, db)\
                and\
            order_services.order_exists(order_id, db):
                order_item_services.delete_order_item_record(order_id, db)
        
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))


