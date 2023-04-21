from decouple import config
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse

from ...constants import api_msgs
from ...exceptions.custom_http_exception import CustomHTTPException
from ...schemas import order_schema
from ...services import order_item_services, order_services, product_item_services
from ...utils.dependencies import *
from ...utils.line_pay.line_pay import check_status, line_pay_request_payment
from ...utils.router_settings import get_path_decorator_settings, get_router_settings

_,protected_singular,_,_ = get_router_settings(
    singular_prefix = 'line-pay',
    plural_prefix = 'line-pays',
    tags = ['line-pay']
)

@protected_singular.post(
    "/request-payment",    
    **get_path_decorator_settings(
        description="create order and request line-pay Request API"
    )
)
def line_pay_payment(
    req: Request,
    payload: order_schema.OrderCreateSchema,
    db:Session = Depends(db.get_db)
):
    try:
        order_id = order_services.create_order(req, payload, db, need_id= True)

        url = line_pay_request_payment(
            order_id,
            payload.total,
            payload.order_items
        )

        RedirectResponse(url=url)

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))



@protected_singular.get(
    "/check-payment-status",
    **get_path_decorator_settings(
        description= "after successfully paid,the page will be directed to this url,and it will check if the order has been paid or not.",
        response_model= list[order_schema.OrderItemSchema]
    )
)
def line_pay_check_payment_status(
    transaction_id: str = Query(..., alias='transactionId'),
    order_id: str = Query(..., alias='orderId'),
    db:Session = Depends(db.get_db)
):
    try:
        order = order_services.get_order_or_raise_not_found(order_id, db)
        total = order.total

        conf_data = {
            "amount": total,
            "currency": "TWD"
        }
        check_status(transaction_id, conf_data)
          
    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))
