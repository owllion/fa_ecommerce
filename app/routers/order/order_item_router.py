from fastapi import Depends, HTTPException, status

from ...constants import api_msgs
from ...exceptions.custom_http_exception import CustomHTTPException
from ...schemas import order_schema
from ...services import order_item_services, order_services, product_item_services
from ...utils.depends.dependencies import *
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="order-item", plural_prefix="order-items", tags=["order-item"]
)


@protected_plural.get(
    "/{order_id}",
    **get_path_decorator_settings(
        description="Get the specific order's order items",
        response_model=list[order_schema.OrderItemSchema],
    )
)
def get_order_items(order_id: str, db: Session = Depends(db.get_db)):
    try:
        order = order_services.get_order_or_raise_not_found(order_id, db)
        return order.order_items

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_singular.delete(
    "/",
    **get_path_decorator_settings(
        description="Successfully delete the order item.",
    )
)
def delete_order_item(
    payload: order_schema.OrderItemDeleteSchema, db: Session = Depends(db.get_db)
):
    product_id, order_id, size = payload.product_id, payload.order_id, payload.size.value

    try:
        order_item = order_item_services.get_order_item_or_raise_not_found(
            order_id, product_id, size, db
        )

        order_item_services.delete_order_item_record(order_item, db)

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))
