from sqlalchemy.orm import Session
from fastapi import Depends
from ..models import item as item_model,user as user_model
from ..schemas import item as item_schema,user as user_schema
from ..database import db

def get_user(*,db: Session=Depends(db.get_db), user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(*,db: Session=Depends(db.get_db), email: str):
    return db.query(user_model.User.User).filter(user_model.User.User.email == email).first()


def get_users(*,db: Session=Depends(db.get_db), skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all() #為啥這邊return會是Schema的User type?這邊不都寫了是user_model的?!?!?


def create_user(*, db: Session = Depends(db.get_db), user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = user_model.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user) #喔是創建的時候要用pydantic的model喔...
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(*,db: Session=Depends(db.get_db), skip: int = 0, limit: int = 100):
    return db.query(item_model.Item).offset(skip).limit(limit).all()


def create_user_item(*, db: Session=Depends(db.get_db), item: item_schema.ItemCreate, user_id: int):
    #為啥傳入的item部會直接是db model的???為啥匯市pydantic model?? 
    db_item = item_model.Item(**item.dict(), owner_id=user_id)
    # we pass the extra keyword argument owner_id that is not provided by the Pydantic model, with:

    item_model.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item