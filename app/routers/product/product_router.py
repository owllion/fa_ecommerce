import json
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi import exceptions as es
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, asc, desc, func

from ...constants import api_msgs, exceptions
from ...exceptions.custom_http_exception import CustomHTTPException
from ...models.product import product_item_model, product_model, size_model
from ...schemas import product_item_schema, product_schema
from ...services import product_services
from ...utils.depends.dependencies import *
from ...utils.redis import keys
from ...utils.redis.keys import (
    best_selling_products_key,
    number_of_search_result_key,
    products_key,
    search_options_key,
)
from ...utils.redis.query.product import deserialize, serialize
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
def get_product(req: Request, product_id: str, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis

        cached_product = client.json().get(products_key(product_id), ".")
        if cached_product:
            print("從cached拿")
            return json.loads(cached_product)

        product = product_services.get_populated_product_or_raise_not_found(product_id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=api_msgs.PRODUCT_NOT_FOUND
            )
        # --------------試驗區
        # images = jsonable_encoder(product.images)
        # thumbnails = jsonable_encoder(product.thumbnails)
        # reviews = jsonable_encoder(product.reviews)
        # print(images, "這是jsonable product的image")
        # print(thubmbnails, "這是jsonable product的thubnails")
        # print(reviews, "這是jsonable product的reviews")
        # -------------

        # res = {
        #     **jsonable_encoder(product),
        #     "images": images,
        #     "thumbnails": thumbnails,
        #     "reviews": reviews,
        # }

        client.json().set(products_key(product_id), ".", json.dumps(jsonable_encoder(product)))
        client.expire(products_key(product_id), timedelta(seconds=300))
        print("過期")
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
        json_payload = jsonable_encoder(payload)
        # client.delete(search_options_key(json.dumps(json_payload)))
        print(number_of_search_result_key(json.dumps(json_payload)), "這是數量key")

        cached_products = client.json().get(search_options_key(json.dumps(json_payload)), ".")
        print(cached_products, "這是cached產品s")
        print(type(cached_products), "這是type")  # str
        cached_total = client.get(number_of_search_result_key(json.dumps(json_payload)))

        if cached_products and cached_total:
            # print(cached_res, "這是cache hash")
            # print(type(cached_res), "這是type")
            # print(type(json.loads(cached_products)), "這是 loads type")  # list

            print(int(cached_total), "總cache比數")

            # deserialize_list = map(lambda x: deserialize.deserialize(x), json.loads(cached_res))
            # print(len(json.loads(cached_res)), "長度")

            res = {"list": json.loads(cached_products), "total": int(cached_total)}
            print("跑cached")
            return res

        query = db.query(product_model.Product)

        total, filtered_list = product_services.filter_products(query, payload).values()

        # print(filtered_list, "這是filter list")
        # client.json().set(
        #     search_options_key(json.dumps(json_payload)), ".", json.dumps(filtered_list)
        # )

        if not filtered_list:
            res = {"list": [], "total": 0}
        else:
            res = {"list": filtered_list, "total": total}

            dict_products = list(map(lambda x: jsonable_encoder(x), filtered_list))
            # print(dict_products, "這是redforredis")

            # print(json.dumps(dict_products), "json畫的res for redis")
            print("資料下面")

            # client.delete(search_options_key(json.dumps(json_payload)))
            # client.json().set(search_options_key(json.dumps(json_payload)), ".", dict_products)
            # --------------------
            # 要設定新搜尋結果
            client.json().set(
                search_options_key(json.dumps(json_payload)), ".", json.dumps(dict_products)
            )
            rrr = client.json().get(search_options_key(json.dumps(json_payload)), ".")
            print(rrr, "這是搜尋結果儲存結果")
            print("設定搜節下面")
            # 搜尋結果expire
            client.expire(search_options_key(json.dumps(json_payload)), timedelta(seconds=3600))

            # 設定筆數(string)
            client.set(number_of_search_result_key(json.dumps(json_payload)), str(total))
            print("設定比數下面")

            cached_total = client.get(number_of_search_result_key(json.dumps(json_payload)))
            print(cached_total, "這是reids存的總筆數")
            # 搜尋結果expire
            client.expire(
                number_of_search_result_key(json.dumps(json_payload)), timedelta(seconds=3600)
            )
            # --------------------------------
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


@public_plural.get(
    "/best-seller",
    **get_path_decorator_settings(
        description="Successfully obtained a list of the top-selling products.",
        response_model=list[product_item_schema.BestSellerProductSchema],
    )
)
def get_top_selling_products(req: Request, db: Session = Depends(db.get_db)):
    try:
        client = req.app.state.redis
        cached_products = client.json().get(best_selling_products_key(), ".")

        if cached_products:
            print("沒有過期")
            print(cached_products, "這是cached priduct")
            return cached_products

        product_items = (
            db.query(product_item_model.ProductItem)
            .order_by(desc(getattr(product_item_model.ProductItem, "sales")))
            .limit(10)
            .all()
        )
        # 這邊不用getattr會error
        """
        Can't resolve label reference for ORDER BY / GROUP BY / DISTINCT etc. Textual SQL expression 'sales' should be explicitly declared as text('sales')"
        """

        dict_products = list(map(lambda x: jsonable_encoder(x.parent_product), product_items))

        print(dict_products, "這是dict products")

        client.json().set(best_selling_products_key(), ".", dict_products)
        client.expire(best_selling_products_key(), timedelta(seconds=600))
        print("過期囉")

        return dict_products

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
