from fastapi import Depends
from sqlalchemy import and_, asc, desc, func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ..database import db
from ..models.product import product_model
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

def get_filters(payload: product_schema.PaginateProductsSchema):
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
                product_model.Product.category == payload.categories
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
        min_, max_ = get_price_range(payload.price).values()
        
        filters.append(and_(product_model.Product.price >= min_, product_model.Product.price <= max_))
    
    return filters

def results_need_sorting(sort_by: str,order_by: str):
    return True if sort_by and order_by else False 


def filter_products(query: Query, payload: product_schema.PaginateProductsSchema):
    """
    Check if the payload has passed the filter condition, and then decide whether to append it to the filters list or not. Finally, perform the query with multiple conditions and return the query results.
    """
    filters = get_filters(payload)

    offset = (payload.page - 1) * payload.limit

    if results_need_sorting(payload.sort_by,payload.order_by):
        order_by_fn = desc if payload.order_by == 'desc' else asc

        sorted_results = query\
            .filter(*filters)\
            .order_by(
                order_by_fn(getattr(product_model.Product,payload.sort_by))
            )\
            .offset(offset)\
            .limit(payload.limit)

        return {
            'total': sorted_results.count(),
            'list': sorted_results.all()
        }
        
    else:
    
        unsorted_results = query\
            .filter(*filters)\
            .offset(offset)\
            .limit(payload.limit)

        return {
            'total': unsorted_results.count(),
            'list': unsorted_results.all()
        }
    
       



