from decouple import config
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse

from ...constants import api_msgs
from ...exceptions.custom_http_exception import CustomHTTPException
from ...models.order import paymant_url_model
from ...schemas import order_schema
from ...schemas.order_schema import PaymentMethods, PaymentStatus
from ...services import order_item_services, order_services, product_item_services
from ...utils.dependencies import *
from ...utils.line_pay.line_pay import check_payment_status, line_pay_request_payment
from ...utils.router_settings import get_path_decorator_settings, get_router_settings

_,protected_singular,_,public_singular = get_router_settings(
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
        #建立訂單
        order = order_services.create_order(req, payload, db, need_order= True)
        print(order.id,'這是order_idddd')
        
        #改paymentMethod
        #要在這改，不然他沒付款就直接跑去看訂單就會變成credit card
        order.payment_method = PaymentMethods.line_pay

        #取得付款連結
        url = line_pay_request_payment(
            order.id,
            payload.total,
            order.order_items
        )
        print(url,'這是下面url')

        #新增payment_url
        payment_url = paymant_url_model.PaymentUrl(
            order_id = order.id,
            url = url
        )
        db.add(payment_url)
        db.commit()
        db.refresh(payment_url)

        return RedirectResponse(url=url)
    

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))



@public_singular.get(
    "/check-payment-status",
    **get_path_decorator_settings(
        description= "after successfully paid,the page will be directed to this url,and it will check if the order has been paid or not.",
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
            "amount": int(total),
            "currency": "TWD"
        }
        print(conf_data,'這是conf_data')
        
        has_paid = check_payment_status(transaction_id,conf_data)
        print(has_paid,"這是has_paid")
        #update_order_status
        if has_paid:
            order.payment_status = PaymentStatus.PAID.value
                        
            db.commit()

        #導回首頁
        return RedirectResponse("http://localhost:3000/")

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(detail= str(e))