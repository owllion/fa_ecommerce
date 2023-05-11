import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi import exceptions as es
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func

from ...constants import api_msgs, exceptions
from ...exceptions.custom_http_exception import CustomHTTPException
from ...models.product import product_item_model, product_model, size_model
from ...schemas import product_schema
from ...services import product_services
from ...utils.depends.dependencies import *
from ...utils.redis import keys
from ...utils.redis.keys import search_options_key
from ...utils.redis.query.product import deserialize, serialize
from ...utils.redis.query.product.search import search_products
from ...utils.router.router_settings import (
    get_path_decorator_settings,
    get_router_settings,
)

protected_plural, protected_singular, public_plural, public_singular = get_router_settings(
    singular_prefix="product", plural_prefix="products", tags=["product"]
)


@protected_singular.post(
    "/",
    **get_path_decorator_settings(
        description="Successfully create product.", response_model=product_schema.ProductSchema
    )
)
def create_product(payload: product_schema.ProductCreateSchema, db: Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_name(payload.product_name, db)

        if product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_ALREADY_EXISTS
            )

        new_product = product_services.save_to_db_then_return(payload, db)

        return new_product

    except Exception as e:
        if type(e).__name__ == exceptions.HTTPException:
            raise e
        raise CustomHTTPException(detail=str(e))


@public_singular.get(
    "/{product_id}",
    **get_path_decorator_settings(
        description="Get the data of a single product.",
        response_model=product_schema.SingleProductSchema,
    )
)
async def get_product(req: Request, product_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis
        # 存到hash裡面orstr都可 沒有要搜尋 皆可
        cached_product = client.get("product_id:")
        if cached_product:
            return cached_product

        product = product_services.find_product_with_id(product_id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_NOT_FOUND
            )
        await client.set(keys.products_key(product.id), json.dumps(product))

        return product

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@public_plural.post(
    "/",
    **get_path_decorator_settings(
        description="Get the product list",
        response_model=product_schema.ResponsePaginateProductsSchema,
    )
)
async def get_products(
    req: Request, payload: product_schema.PaginateProductsSchema, db: Session = Depends(db.get_db)
):
    try:
        client = req.app.state.redis
        print(client, "這是client")
        json_payload = jsonable_encoder(payload)

        cached_res = client.json().get(search_options_key(json.dumps(json_payload)))
        if cached_res:
            # print(cached_res, "這是cache hash")
            # print(type(cached_res), "這是type")
            print(type(json.loads(cached_res)), "這是 loads type")  # list

            # deserialize_list = map(lambda x: deserialize.deserialize(x), json.loads(cached_res))
            print(len(json.loads(cached_res)), "長度")
            res = {"list": json.loads(cached_res), "total": len(json.loads(cached_res))}
            print("跑cached")
            return res

        query = db.query(product_model.Product)

        total, filtered_list = product_services.filter_products(query, payload).values()

        print(filtered_list, "這是filter list")
        # client.json().set(
        #     search_options_key(json.dumps(json_payload)), ".", json.dumps(filtered_list)
        # )

        if not filtered_list:
            res = {"list": [], "total": 0}
        else:
            res = {"list": filtered_list, "total": total}
            res_for_redis = list(map(lambda x: jsonable_encoder(x), filtered_list))
            print(res_for_redis, "這是redforredis")
            # 這邊都沒問題

            print(json.dumps(res_for_redis), "json畫的res for redis")

            client.json().set(
                search_options_key(json.dumps(json_payload)), ".", json.dumps(res_for_redis)
            )

            # result = client.json().get(search_options_key(json.dumps(json_payload)))
            # print(result, "這是result")

            # await client.json(
            #     search_options_key(json.dumps(json_payload)), json.dumps(res_for_redis)
            # )

        return res

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_singular.put(
    "/",
    **get_path_decorator_settings(
        description="Successfully update the product.",
    )
)
def update_product(payload: product_schema.ProductUpdateSchema, db: Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(payload.id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_NOT_FOUND
            )

        data = payload.dict(exclude_unset=True)

        for field, value in data.items():
            if hasattr(product, field):
                setattr(product, field, value)

        db.commit()

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


@protected_singular.delete(
    "/{product_id}",
    **get_path_decorator_settings(
        description="Successfully delete the product.",
    )
)
def delete_product(product_id: str, db: Session = Depends(db.get_db)):
    try:
        product = product_services.find_product_with_id(product_id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_NOT_FOUND
            )

        db.delete(product)

        db.commit()

    except Exception as e:
        if isinstance(e, (HTTPException,)):
            raise e
        raise CustomHTTPException(detail=str(e))


# @public_router.put("/{product_id}")
# async def update_item(product_id: str):
#     return {'name': 'hello'}
# #     stored_item_data = items[item_id]
# #     stored_item_model = Item(**stored_item_data)
# #     update_data = item.dict(exclude_unset=True)
# #     updated_item = stored_item_model.copy(update=update_data)
# #     items[item_id] = jsonable_encoder(updated_item)
# #     return updated_item
