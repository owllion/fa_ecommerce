import json

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ...constants import api_msgs
from ...exceptions.custom_http_exception import CustomHTTPException
from ...schemas import order_schema
from ...services import order_services
from ...utils.depends.dependencies import *
from ...utils.redis.keys import user_orders_key
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="order", plural_prefix="orders", tags=["order"]
)


@protected_singular.post(
    "/", **get_path_decorator_settings(description="Successfully create the order.")
)
def create_order(
    req: Request, payload: order_schema.OrderCreateSchema, db: Session = Depends(db.get_db)
):
    try:
        order_services.create_order(req, payload, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_singular.get(
    "/{order_id}",
    **get_path_decorator_settings(
        description="Get the data of a order", response_model=order_schema.OrderSchema
    )
)
def get_order(order_id: str, db: Session = Depends(db.get_db)):
    try:
        order = order_services.get_order_or_raise_not_found(order_id, db)
        return order

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_plural.get(
    "/",
    **get_path_decorator_settings(
        description="Get the order list", response_model=list[order_schema.OrderSchema]
    )
)
async def get_orders(db: Session = Depends(db.get_db)):
    try:
        orders = await order_services.get_all_orders(db)
        return orders

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_plural.get(
    "/user/{user_id}",
    **get_path_decorator_settings(
        description="Get the specific user's order list",
        response_model=list[order_schema.OrderWithoutItemsSchema],
    )
)
def get_user_orders(req: Request, user_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis
        cached_orders = client.json().get(user_orders_key(user_id))
        if cached_orders:
            print(type(cached_orders), "這是cacehd order type")
            return json.loads(cached_orders)

        orders = order_services.get_orders_by_user_id(user_id, db)
        print(orders[1].payment_method, "這是拿到的orders")
        print(orders[1].id, "這是拿到的order  id")
        for order in orders:
            if order.id == "251801d99ee0439697fe0bd7839b506e":
                print(order.payment_url.url, "這是付款連結")
        # json_orders = list(map(lambda x: jsonable_encoder(x), orders))
        # print(json_orders, "這是json_orders")

        # client.json().set(user_orders_key(user_id), ".", json.dumps(json_orders))
        # # orm obj要先轉乘一班dict才可以被json化
        # cached_orders = client.json().get(user_orders_key(user_id))
        # print(cached_orders, "這是cached_orders")
        return orders

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description="Successfully update the order.",
    )
)
async def update_order(payload: order_schema.OrderUpdateSchema, db: Session = Depends(db.get_db)):
    try:
        order = await order_services.get_order_or_raise_not_found(payload.id, db)

        await order_services.update_order_record(payload, order, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_singular.delete(
    "/{order_id}",
    **get_path_decorator_settings(
        description="Successfully delete the order.",
    )
)
async def delete_order(order_id: str, db: Session = Depends(db.get_db)):
    try:
        await order_services.delete_order_record(order_id, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))
