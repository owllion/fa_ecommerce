from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..constants import api_msgs, exceptions
from ..exceptions.http_exception import CustomHTTPException
from ..schemas import product_schema
from ..services import product_services
from ..utils.dependencies import *
from ..utils.router_settings import get_path_decorator_settings, get_router_settings

protected_router = APIRouter(**get_router_settings(
  {
    'is_protected': True,
    'prefix': '/product',
    'tags': ['product'],
    'responses': {404: {"description": "Not found"}}
  }  
))

public_router = APIRouter(**get_router_settings(
  {
    'is_protected': False,
    'prefix': '/product',
    'tags': ['product'],
    'responses': {404: {"description": "Not found"}}
  }  
))

@protected_router.post(
    "/", 
    **get_path_decorator_settings(
        description= "Successfully create product.",
        response_model= product_schema.ProductSchema
    )
)
def create_product(payload: product_schema.ProductCreateSchema, db: Session = Depends(db.get_db)):
    
    try:
        product = product_services.find_product_with_name(payload.product_name, db)
        
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

@public_router.get(
    "/{product_id}",
    **get_path_decorator_settings(
        description= "Get the data of a single product.",
        response_model= product_schema.ProductSchema
    )
)
def get_product(product_id: str,db:Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(product_id,db)

        if not product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= api_msgs.PRODUCT_NOT_FOUND
            )
        
        return jsonable_encoder(product)
    
                
    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException: raise e
        raise CustomHTTPException(detail= str(e))



@protected_router.put(
    "/",
    **get_path_decorator_settings(
        description= "Successfully update the product.",
    )
)
def update_product(
    req: Request,
    payload: product_schema.ProductUpdateSchema,
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



# @public_router.put("/{product_id}")
# async def update_item(product_id: str):
#     return {'name': 'hello'}
# #     stored_item_data = items[item_id]
# #     stored_item_model = Item(**stored_item_data)
# #     update_data = item.dict(exclude_unset=True)
# #     updated_item = stored_item_model.copy(update=update_data)
# #     items[item_id] = jsonable_encoder(updated_item)
# #     return updated_item

