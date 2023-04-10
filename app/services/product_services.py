from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import db
from ..models.product import product_image_url_model, product_model
from ..schemas import product_schema


def find_product_with_id(
    id: str,
    db: Session = Depends(db.get_db)
):
    product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    
    return product

def save_to_db_then_return(
    payload: product_schema.ProductCreateSchema, 
    db: Session = Depends(db.get_db)
):
    new_product = product_model.Product(**payload.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product