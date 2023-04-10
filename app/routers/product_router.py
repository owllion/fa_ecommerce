from fastapi import APIRouter, Depends, HTTPException, status

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
        product = product_services.find_product_with_id(payload.id)
        
        if product: 
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail = api_msgs.PRODUCT_ALREADY_EXISTS
            )
        
        new_product = product_services.save_to_db_then_return(product,db)
        
        return new_product


    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException:
            raise e
        raise CustomHTTPException(detail= str(e))




@public_router.put("/{product_id}")
async def update_item(product_id: str):
    return {'name': 'hello'}
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item

#protected - 新增/刪除/修改 
#public - 查詢單一商品/查詢商品列表
