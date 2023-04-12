from fastapi import Depends
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ..database import db
from ..models.product import product_image_url_model, product_model
from ..schemas import product_schema


def find_product_with_name(
    name: str,
    db: Session = Depends(db.get_db)
):
    product = db.query(product_model.Product).filter(product_model.Product.product_name == name).first()
    
    return product

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


def get_price_range(price: str):
  return {
    'min_': int(price[:price.index("-")]) or 0,
    'max_': int(price[price.index("-") + 1:]) or 0,
  }

def filter_products(query: Query, payload: product_schema.PaginateProductsSchema):
    filters = []

    if payload.keyword:
        keyword = payload.keyword.lower().strip()

        filters.append(
            func.lower(product_model.Product.product_name).like(f'%{keyword}%')
        )

    if payload.categories:
        if isinstance(payload.categories,list):
            filters.append(
                product_model.Product.category.in_(payload.categories)
            )
        else: #category is a str
            filters.append(
                product_model.Product.category == payload.categories)
            )
           

    if payload.brands:
        if isinstance(payload.brands,list):
            filters.append(
                product_model.Product.brand.in_(payload.brands)
            )
        else: #brand is a str
            filters.append(
                product_model.Product.brand == payload.brands
            )

    if payload.price:
        min_, max_ = get_price_range(payload.price)
        print(min_,'這是min')
        print(max_,'這是max')
        
        filters.append(and_(product_model.Product.price >= min_, product_model.Product.price <= max_))
    
    return query.filter(*filters)



   