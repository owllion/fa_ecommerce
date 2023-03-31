
from jose import JWTError,ExpiredSignatureError,jwt
from datetime import datetime,timedelta

def create_token():
    expire = datetime.utcnow() + timedelta(minutes=30)
    
    token = jwt.encode(
        claims = {
            "exp": expire, 
            "user_id":"123456798"
        },
        key = "mySecret", 
        algorithm= "HS256"
    )
    print(token,'this is token')

    return token
create_token()