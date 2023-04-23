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
from .get_signature import get_signature

channel_id = config('LINEPAY_CHANNEL_ID')
channel_secret = config('LINEPAY_CHANNEL_SECRET_KEY')
uri = "/v3/payments/request"
nonce = str(round(time.time() * 1000))  # nonce = str(uuid.uuid4())
print(nonce,'nonce被呼叫!')
transaction_id = ''



def gen_package_products(order_items: list[OrderItemSchema]):
    res = []
    for item in order_items:
        item = {
            "name": item.product_info.product_name,
            "quantity": item.qty,
            "price": int(item.product_info.price),
            "imageUrl": item.product_info.thumbnail
        }
        res.append(item)

    return res


def get_req_body(
    total: float,
    order_id: str,
    order_items: list[OrderItemSchema]
):
    confirm_url = f"{config('LINEPAY_RETURN_HOST')}/{config('LINEPAY_RETURN_CONFIRM_URL')}"
    
    print(total,'這是total')

    body = {
        "amount": int(total),
        "currency": 'TWD',
        "orderId": order_id,
        "packages": [{
            "id": str(uuid.uuid4()),
            "amount": int(total),
            "name": config("SHOP_NAME")
        }],
        "redirectUrls": {
            "confirmUrl": confirm_url,
            "cancelUrl": ""
        }
    }

    body['packages'][0]['products'] = gen_package_products(order_items)

    print(body['packages'][0]['products'],'這是products')

    return body
        

request_options = {
        "amount": 2000,
        "currency": 'TWD',
        "orderId": nonce,
        "packages": [{
            "id": '20220314I001',
            "amount": 2000,
            "name": '鬼滅之刃公仔',
            "products": [{
                "name": '竈門禰豆子',
                "quantity": 1,
                "price": 1000
            },{
                "name": '我妻善逸',
                "quantity": 1,
                "price": 1000
            }]
        }],
        "redirectUrls": {
            "confirmUrl": '',
            "cancelUrl": ''
        }
    }
def get_auth_signature (secret, uri, body, nonce):
    """
    用於製作密鑰
    :param secret: your channel secret
    :param uri: uri
    :param body: request body
    :param nonce: uuid or timestamp(時間戳)
    :return:
    """
    str_sign = secret + uri + body + nonce
    return base64.b64encode(hmac.new(str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256).digest()).decode("utf-8")

def get_signature(secret, uri, body, nonce):

    message = secret + uri + body + nonce
    
    hash = hmac.new(
        str.encode(secret), 
        str.encode(message), 
        digestmod= hashlib.sha256
    ).digest()

    signature = base64.b64encode(hash).decode('utf-8')

    return signature



headers = {
    'Content-Type': 'application/json',
    'X-LINE-ChannelId': channel_id,
}


def get_dict_data(res: requests.Response):
    res_text = res.text
    return json.loads(res_text)


def get_redirect_url(data):
    url = data.get('info').get('paymentUrl').get('web')
    return url

def do_request_payment(
        total: float,
        order_id: str,
        order_items: list[OrderItemSchema],
        nonce: str
    ):

    nonce = gen_nonce()
    print("進入 do_request_payment")
    json_body = json.dumps(get_req_body(total, order_id, order_items))
    print(json_body,'這是jsonbody喔')
    print(nonce,'這是nonce(在耕莘header之前)')
    headers['X-LINE-Authorization-Nonce'] = nonce
    headers['X-LINE-Authorization'] = get_auth_signature(secret=channel_secret, uri = uri, body=json_body, nonce=nonce)

    response = requests.post(
       "https://sandbox-api-pay.line.me"+ uri, 
       headers= headers, 
       data= json_body
    )
    return response

def get_transaction_id(data):
    return data.get('info').get('transactionId')

def line_pay_request_payment(
    order_id: str, 
    total: float, 
    order_items: list[OrderItemSchema]
):
    print("進入line_pay_request_payment")
    response = do_request_payment(
        total,
        order_id,
        order_items,
        nonce,
    )

    data = get_dict_data(response)
    print(data,'這是data')
    print(data.get("returnCode"),'這是回傳code')
    if data.get("returnCode") == '0000':
        url = get_redirect_url(data)
        transaction_id = get_transaction_id(data)

        print(f"重新導向的連結: {url}")
        print(f"交易序號: {transaction_id}")
    
    return url


# def do_request_payment2():
#     '''此api僅使用文檔中必填的資料'''
    

#     json_body = json.dumps(request_options)


#     headers['X-LINE-Authorization-Nonce'] = nonce

#     headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, uri, json_body, nonce)

#     response = requests.post("https://sandbox-api-pay.line.me"+uri, headers=headers, data=json_body)

#     print(response.text)
#     dict_response = json.loads(response.text)

#     if dict_response.get('returnCode') == "0000":
#         info = dict_response.get('info')

#         web_url = info.get('paymentUrl').get('web')

#         transaction_id = str(info.get('transactionId'))

#         print(f"付款web_url:{web_url}")
#         print(f"交易序號:{transaction_id}")

def check_payment_status(transaction_id: str, conf_data: dict[str, str| float]):
    
    # conf_data = """{"amount": 450, "currency": "TWD"}"""
    nonce = gen_nonce()
    checkout_url = f"/v3/payments/requests/{transaction_id}/check"
    
    print(json.dumps(conf_data),'這是json畫之後的')

    headers['X-LINE-Authorization-Nonce'] = nonce
    headers['X-LINE-Authorization'] = get_auth_signature(secret=channel_secret, uri = checkout_url, body=json.dumps(conf_data),nonce=nonce)

    response = requests.get(
        "https://sandbox-api-pay.line.me"+ checkout_url, headers=headers, 
        data=json.dumps(conf_data)
    )

    print(response.text,'這是response.text')

    response = json.loads(response.text)

    if str(response.get('returnCode')) == "0110":
        return True
    return False

def do_confirm(transaction_id):

    con_url = f"/v3/payments/{transaction_id}/confirm"
    conf_data = """{"amount": 2000, "currency": "TWD"}"""
    headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, con_url, conf_data, nonce)
    response = requests.post("https://sandbox-api-pay.line.me"+con_url, headers=headers, data=conf_data)
    print(response.text)
    response = json.loads(response.text)

    return response.get('returnMessage')

if __name__ == "__main__":
    print('ee')
    # # do_request_payment2() # 向linepay請求付款

    # line_pay_checkout() # 向linepay請求付款


    # # 填入已付款後的交易序號後下方註解拿掉
    # transaction_id = "2023042101199026710" 

    # status = do_checkout(transaction_id)  # 檢查訂單狀態
    
    # if status :
    #     print(do_confirm(transaction_id))  # 確認訂單
# check_payment_status("2023042301213859810")