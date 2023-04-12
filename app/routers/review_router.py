from fastapi import APIRouter, Depends, HTTPException
from fastapi import exceptions as es
from fastapi import status
from fastapi.encoders import jsonable_encoder

from ..constants import api_msgs, exceptions
from ..exceptions.http_exception import CustomHTTPException
from ..schemas import review_schema
from ..services import review_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_router = APIRouter(**get_router_settings(
  {
    'is_protected': True,
    'prefix': '/review',
    'tags': ['review'],
    'responses': {404: {"description": "Not found"}}
  }  
))

public_router = APIRouter(**get_router_settings(
  {
    'is_protected': False,
    'prefix': '/review',
    'tags': ['review'],
    'responses': {404: {"description": "Not found"}}
  }  
))

@protected_router.post(
    "/", 
    **get_path_decorator_settings(
        description= "Successfully create product.",
        response_model= review_schema.reviewSchema
    )
)
def create_review(payload: review_schema.reviewCreateSchema, db: Session = Depends(db.get_db)):
    
    try:
        review = review_services.find_review_with_name(payload.product_name, db)
        
        if product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail = api_msgs.PRODUCT_ALREADY_EXISTS
            )
        
        new_product = product_services.save_to_db_then_return(payload,db)
        
        return new_product


    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException:
            raise e
        raise CustomHTTPException(detail= str(e))

# @public_router.get(
#     "/{product_id}",
#     **get_path_decorator_settings(
#         description= "Get the data of a single product.",
#         response_model= review_schema.ProductSchema
#     )
# )
@public_router.get(
    "/{product_id}",
    status_code= status.HTTP_200_OK,
    response_description= ' 哈哈',
    response_model= review_schema.ProductSchema
)
def get_product(product_id: str,db:Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(product_id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        print(product.thumbnails,'外面的thumbnails')
        print(product.color,'這是顏色')
        
        return product
    
                
    except Exception as e:
        #isinstance會檢查繼承關係
        if isinstance(e, exceptions.HTTPException): raise e
        raise CustomHTTPException(detail= str(e))


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

@protected_router.put(
    "/",
    **get_path_decorator_settings(
        description= "Successfully update the product.",
    )
)
def update_product(
    req: Request,
    payload: review_schema.ProductUpdateSchema,
    db:Session = Depends(db.get_db)
):
    try:
        product = product_services.find_product_with_id(payload.id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        
        data = payload.dict(exclude_unset=True)

        for field, value in data.items():
          if hasattr(product, field) :
              setattr(product, field, value)
        
        db.commit()
        
    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException: raise e
        raise CustomHTTPException(detail= str(e))


@protected_router.delete(
    "/{product_id}",
    **get_path_decorator_settings(
        description= "Successfully delete the product.",
    )
)
def delete_product(product_id: str,db:Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(product_id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        
        db.delete(product)
        
        db.commit()
        
    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException: raise e
        raise CustomHTTPException(detail= str(e))


