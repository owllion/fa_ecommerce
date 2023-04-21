import base64
import hashlib
import hmac
import json

from decouple import config

from .generate_nonce import gen_nonce


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
    
    hash = hmac.new(str.encode(secret), str.encode(message), digestmod= hashlib.sha256).digest()

    signature = base64.b64encode(hash).decode('utf-8')

    return signature


def nothing():
    CHANNEL_ID = config('LINE_CHANNEL_ID')
    
    CHANNEL_SECRET = config('LINE_CHANNEL_SECRET_KEY')

    LINEPAY_VERSION = "v3"

    URI = config("REQUEST_API")

    LINEPAY_BODY = {
    "amount": 500,
    "currency": "TWD",
    "orderId": "order20210921003",
    "packages": [
        {
            "id": "20210921003",
            "amount": 500,
            "products": [
                {
                    "name": "買不起的iphone13pro",
                    "quantity": 1,
                    "price": 500
                }
            ]
        }
    ],
    "redirectUrls": {
        "confirmUrl": "http://127.0.0.1:3000/confitmUrl",
        "cancelUrl": "http://127.0.0.1:3000/cancelUrl"
    }
}

    
    print(json.dumps(LINEPAY_BODY),'這是json body')

    nonce = gen_nonce()
    print(nonce,"這是nonce")

    message2 = f"{CHANNEL_SECRET}{URI}{json.dumps(LINEPAY_BODY)}{nonce}"
    message = CHANNEL_SECRET + URI + json.dumps(LINEPAY_BODY) + nonce
    print(message,'這是message')

    # message = message.encode('utf-8')

    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    # encrypt = hash.digest()

    signature = base64.b64encode(hash).decode('utf-8')
    # t = base64.b64encode(hmac.new(str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256).digest()).decode("utf-8")
    print(signature)
    return signature

