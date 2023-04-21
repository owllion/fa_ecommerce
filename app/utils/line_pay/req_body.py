
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
            "confirmUrl": 'https://quietbo.com/2022/03/14/python-linepay%e4%b8%b2%e6%8e%a5online-apis-%e5%95%8f%e9%a1%8c-5-5/',
            "cancelUrl": 'https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/'
        }
    }