import time
import uuid

from decouple import config


def gen_nonce():
    nonce = str(uuid.uuid4())
    return nonce
