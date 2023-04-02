from fastapi import APIRouter, Depends, HTTPException

from ..utils.dependencies import *

public_router = APIRouter(
    prefix="/product",
    tags=["product_public"],
    responses={404: {"description": "Not found"}},
)

protected_router = APIRouter(
    prefix="/product",
    tags=["product_protected"],
    dependencies=[Depends(validate_token)],
    responses={404: {"description": "Not found"}},
)

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
