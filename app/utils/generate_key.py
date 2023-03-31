import base64
from decouple import config

def generate_key():
    return base64.b64decode(
       config('JWT_SECRET').decode('utf-8')
    )