import re

import aioredis

from .....schemas.product_schema import PaginateProductsSchema
from .....services.product_services import get_price_range
from ...keys import products_index_key
from .deserialize import deserialize


async def search_products(redis: aioredis.Redis, payload: PaginateProductsSchema):
    # 先過濾關鍵字(可以是空的，但其他欄位友直)，所以不用特別處理空白的狀態，(因為前端觸發搜尋是多點的，勾選的、單選的都會觸發，所以keyword可能空白!)
    # 只需處理keyword和其他所有條件也都是None的情況啦(但這樣根本不會觸發搜尋阿XD)

    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", payload.keyword)

    # 過濾完成後就寫query
    # 1.判斷brand、categories是否為list/None/str再去做出對應寫法(None不用寫，list就維持，str要放入list中)
    # 2.price是numeric，以上filter conditions都依樣，
    if payload.price:
        min_, max_ = get_price_range(payload.price).values()

    if payload.brands:
        if isinstance(payload.brands, list):
            brands = "|".join(payload.brands)
        else:
            brands = payload.brands

    if payload.categories:
        if isinstance(payload.categories, list):
            categories = "|".join(payload.categories)
        else:
            categories = payload.categories

    categorys = "|".join(categorys) if isinstance(payload.categories, list) and categorys else None

    query = f"(@name:({cleaned}) => {'$weight':5.0}) | (@description:({cleaned})) | (@price:[{min_} {max_}]) | (@brand:({{{brands}}})) | category:({{{categories}}}))"

    sort_criteria = (
        {"BY": payload.sortBy, "DIRECTION": payload.direction}
        if payload.sortBy and payload.direction
        else None
    )
    total, document = await redis.ft(products_index_key()).search(query)

    return {
        "total": total,
        "list": map(lambda x: deserialize(x["id"].replace("products#", ""), x["value"]), document),
    }
