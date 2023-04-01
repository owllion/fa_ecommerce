from typing import Annotated
from fastapi import Header, HTTPException,Request,status,Depends
from sqlalchemy.orm import Session
from ..utils.security import decode_token
from ..database.crud import user_crud
from ..database import db
async def get_token_header(req:Request ,authorization: Annotated[str, Header()],db: Session = Depends(db.get_db)):
    token = authorization.replace('Bearer ','')
    decoded_data = decode_token(token,'access',db)
    print(decoded_data,'挖喔')
    
    
    req.state.user = decoded_data