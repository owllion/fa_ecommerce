import base64
import hashlib
import hmac
import json
import time
import uuid

import requests
from decouple import config

from ...schemas.order_schema import OrderCreateSchema, OrderItemSchema
from .generate_nonce import gen_nonce

channel_id = config("LINEPAY_CHANNEL_ID")
channel_secret = config("LINEPAY_CHANNEL_SECRET_KEY")
uri = "/v3/payments/request"
nonce = str(round(time.time() * 1000))
transaction_id = ""


def gen_package_products(order_items: list[OrderItemSchema]):
    res = []
    for item in order_items:
        item = {
            "name": item.product_info.product_name,
            "quantity": item.qty,
            "price": int(item.product_info.price),
            "imageUrl": item.product_info.thumbnail,
        }

        res.append(item)

    return res


def get_req_body(total: float, order_id: str, order_items: list[OrderItemSchema]):
    confirm_url = f"{config('LINEPAY_RETURN_HOST')}/{config('LINEPAY_RETURN_CONFIRM_URL')}"

    body = {
        "amount": int(total),
        "currency": "TWD",
        "orderId": order_id,
        "packages": [{"id": str(uuid.uuid4()), "amount": int(total), "name": config("SHOP_NAME")}],
        "redirectUrls": {"confirmUrl": confirm_url, "cancelUrl": ""},
    }

    body["packages"][0]["products"] = gen_package_products(order_items)

    return body


def get_auth_signature(secret, uri, body, nonce):
    str_sign = secret + uri + body + nonce
    return base64.b64encode(
        hmac.new(str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256).digest()
    ).decode("utf-8")


headers = {
    "Content-Type": "application/json",
    "X-LINE-ChannelId": channel_id,
}


def get_dict_data(res: requests.Response):
    res_text = res.text
    return json.loads(res_text)


def get_redirect_url(data):
    url = data.get("info").get("paymentUrl").get("web")
    return url


def do_request_payment(
    total: float, order_id: str, order_items: list[OrderItemSchema], nonce: str
):
    nonce = gen_nonce()

    json_body = json.dumps(get_req_body(total, order_id, order_items))

    headers["X-LINE-Authorization-Nonce"] = nonce
    headers["X-LINE-Authorization"] = get_auth_signature(
        secret=channel_secret, uri=uri, body=json_body, nonce=nonce
    )

    response = requests.post(
        "https://sandbox-api-pay.line.me" + uri, headers=headers, data=json_body
    )
    return response


def get_transaction_id(data):
    return data.get("info").get("transactionId")


def line_pay_request_payment(order_id: str, total: float, order_items: list[OrderItemSchema]):
    response = do_request_payment(
        total,
        order_id,
        order_items,
        nonce,
    )

    data = get_dict_data(response)

    if data.get("returnCode") == "0000":
        url = get_redirect_url(data)

    return url


def check_payment_status(transaction_id: str, conf_data: dict[str, str | float]):
    nonce = gen_nonce()
    checkout_url = f"/v3/payments/requests/{transaction_id}/check"

    headers["X-LINE-Authorization-Nonce"] = nonce
    headers["X-LINE-Authorization"] = get_auth_signature(
        secret=channel_secret, uri=checkout_url, body=json.dumps(conf_data), nonce=nonce
    )

    response = requests.get(
        "https://sandbox-api-pay.line.me" + checkout_url,
        headers=headers,
        data=json.dumps(conf_data),
    )

    response = json.loads(response.text)

    if str(response.get("returnCode")) == "0110":
        return True
    return False
