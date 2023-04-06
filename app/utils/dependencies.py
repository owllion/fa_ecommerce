from typing import Annotated

from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session

from ..database import db
from ..utils.security import decode_token


async def validate_token(req:Request ,authorization: Annotated[str, Header()],db: Session = Depends(db.get_db)):
    #no need to check if there is authorization token or not, coz if we do not pass the token, fastApi will directly response 422 error, would not even run a single line in this function.

    token = authorization.replace('Bearer ','')

    decoded_data = decode_token(token,'access',db)
    
    req.state.mydata = decoded_data