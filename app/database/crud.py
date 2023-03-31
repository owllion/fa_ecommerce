from sqlalchemy.orm import Session
from fastapi import Depends
from ..models import item_model,user_model

from ..schemas import item_schema,user_schema
from ..database import db

def get_user(*,db: Session=Depends(db.get_db), user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(*,db: Session=Depends(db.get_db), email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_users(*,db: Session=Depends(db.get_db), skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(*, db: Session = Depends(db.get_db), user: user_schema.UserCreateSchema):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = user_model.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user) 
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