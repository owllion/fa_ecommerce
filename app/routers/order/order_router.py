import json
from datetime import timedelta

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from ...exceptions.main import get_exception
from ...schemas import order_schema
from ...services import order_services
from ...utils.depends.dependencies import *
from ...utils.redis.keys import orders_key, user_orders_key
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
        order_services.svc_create_order(req, payload, db)

    except Exception as e:
        get_exception(e)


@protected_singular.get(
    "/{order_id}",
    **get_path_decorator_settings(
        description="Get the data of a order", response_model=order_schema.OrderSchema
    )
)
def get_order(req: Request, order_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis

        cached_order = client.json().get(orders_key(order_id), ".")

        if cached_order:
            return json.loads(cached_order)

        order = order_services.get_populated_order_or_raise_not_found(order_id, db)

        client.json().set(orders_key(order_id), ".", json.dumps(jsonable_encoder(order)))

        client.expire(orders_key(order_id), timedelta(seconds=600))

        return order

    except Exception as e:
        get_exception(e)


@protected_plural.get(
    "/",
    **get_path_decorator_settings(
        description="Get the order list", response_model=list[order_schema.OrderSchema]
    )
)
def get_orders(db: Session = Depends(db.get_db)):
    try:
        orders = order_services.svc_get_orders(db)

        return orders

    except Exception as e:
        get_exception(e)


@protected_plural.get(
    "/user/{user_id}",
    **get_path_decorator_settings(
        description="Get the specific user's order list",
        response_model=order_schema.ResponseOrder,
    )
)
def get_user_orders(req: Request, user_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis

        cached_orders = client.json().get(user_orders_key(user_id), ".")

        total_len = client.json().arrlen(user_orders_key(user_id), ".")

        if cached_orders and total_len:
            return {"list": cached_orders, "total": total_len}

        orders = req.state.mydata.orders

        json_orders = list(map(lambda x: jsonable_encoder(x), orders))

        client.json().set(user_orders_key(user_id), ".", json_orders)

        client.expire(user_orders_key(user_id), timedelta(seconds=60))

        total_len = client.json().arrlen(user_orders_key(user_id), ".")

        return {"list": orders, "total": total_len}

    except Exception as e:
        get_exception(e)


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description="Successfully update the order.",
    )
)
def update_order(payload: order_schema.OrderUpdateSchema, db: Session = Depends(db.get_db)):
    try:
        order = order_services.get_order_or_raise_not_found(payload.id, db)

        order_services.svc_update_order_record(payload, order, db)

    except Exception as e:
        get_exception(e)


@protected_singular.delete(
    "/{order_id}",
    **get_path_decorator_settings(
        description="Successfully delete the order.",
    )
)
def delete_order(order_id: str, db: Session = Depends(db.get_db)):
    try:
        order_services.svc_delete_order(order_id, db)

    except Exception as e:
        get_exception(e)
