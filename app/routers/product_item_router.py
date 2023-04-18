from fastapi import APIRouter, Depends, HTTPException
from fastapi import exceptions as es
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func

from ..constants import api_msgs, exceptions
from ..exceptions.http_exception import CustomHTTPException
from ..models.product import product_item_model, product_model, size_model
from ..schemas import product_item_schema
from ..services import product_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_plural,protected_singular,public_plural,public_singular = get_router_settings(
    singular_prefix = 'product-item',
    plural_prefix = 'product-items',
    tags = ['product-item']
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
    description= "create a product item",
    response_model= product_item_schema.ProductItemSchema
    )
)
def create_product_item(
    payload: product_item_schema.ProductItemCreateSchema,
    db: Session = Depends(db.get_db)
):
    try:
        product = product_services.find_product_with_id(payload.product_id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        size = db.query(size_model.Size).filter(size_model.Size.id == payload.size_id)

        if not size: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.SIZE_NOT_FOUND
            )
        
        product_item = db.query(product_item_model.ProductItem).filter(
            product_item_model.ProductItem.size_id == payload.size_id,
            product_item_model.ProductItem.product_id == payload.product_id

        ).first()

        print("product_ite", jsonable_encoder(product_item))
        if product_item:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail= api_msgs.PRODUCT_ITEM_ALREADY_EXISTS
            )

        product_item = product_item_model.ProductItem(
            product_id = payload.product_id,
            size_id = payload.size_id,
            stock = payload.stock,
            sales = payload.sales
        )
        db.add(product_item)
        db.commit()

        return product_item

    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(
            detail= str(e)
        )

@protected_singular.delete(
    "/",
    **get_path_decorator_settings(
    description= "delete a product item"
    )
)
def delete_product_item(
    payload: product_item_schema.ProductItemDeleteSchema,
    db: Session = Depends(db.get_db)
):
    try:
        product = product_services.find_product_with_id(payload.product_id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        
        size = db.query(size_model.Size).filter(size_model.Size.id == payload.size_id).first()

        if not size: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.SIZE_NOT_FOUND
            )

        product_item = db.query(product_item_model.ProductItem).filter(
            product_item_model.ProductItem.size_id == payload.size_id,
            product_item_model.ProductItem.product_id == payload.product_id

        ).first()

        if not product_item:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_ITEM_NOT_FOUND
            )
        
        db.delete(product_item)
        db.commit()


    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(
            detail= str(e)
        )


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
    description= "update a product item"
    )
)
def update_product_item(
    payload: product_item_schema.ProductItemUpdateSchema,
    db: Session = Depends(db.get_db)
):
    try:
        
        product = product_services.find_product_with_id(payload.product_id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        
        size = db.query(size_model.Size).filter(size_model.Size.id == payload.size_id).first()

        if not size: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.SIZE_NOT_FOUND
            )
        

        product_item = db.query(product_item_model.ProductItem).filter(
            product_item_model.ProductItem.size_id == payload.size_id,
            product_item_model.ProductItem.product_id == payload.product_id

        ).first()

        if not product_item:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_ITEM_NOT_FOUND
            )
        
        data = payload.dict(exclude_unset=True)

        for field,value in data.items():
            if hasattr(product_item, field):
                setattr(product_item, field, value)
        
        db.commit()


    except Exception as e:
        if isinstance(e, (HTTPException,)): raise e
        raise CustomHTTPException(
            detail= str(e)
        )
    
@public_plural.get(
    "/all",
    **get_path_decorator_settings(
    description= "get the product item list",
    response_model= list[product_item_schema.ProductItemSchema]
    )
)
def get_all_product_items(db: Session = Depends(db.get_db)):
    items = db.query(product_item_model.ProductItem).all()
    return items


@public_plural.get(
    "/product/{product_id}",
    **get_path_decorator_settings(
    description= "get all the product items of specified product.",
    response_model= list[product_item_schema.ProductItemSchema]
    )
)
def get_product_items(product_id: str,db: Session = Depends(db.get_db)):
    items = db.query(product_item_model.ProductItem).filter(product_item_model.ProductItem.product_id == product_id).all()

    return items





















