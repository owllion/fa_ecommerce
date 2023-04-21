import time
import uuid

from decouple import config


def gen_nonce():    
    # nonce = str(uuid.uuid4()) + str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    print(type(nonce),'這是type')
    
    return nonce

