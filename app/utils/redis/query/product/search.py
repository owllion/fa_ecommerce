import re

import aioredis

from .....schemas.product_schema import PaginateProductsSchema
from .....services.product_services import get_price_range
from ...keys import products_index_key
from .deserialize import deserialize


async def search_products(redis: aioredis.Redis, payload: PaginateProductsSchema):
    # 先過濾關鍵字(可以是空的，但其他欄位友直)，所以不用特別處理空白的狀態，(因為前端觸發搜尋是多點的，勾選的、單選的都會觸發，所以keyword可能空白!)
    # 只需處理keyword和其他所有條件也都是None的情況啦(但這樣根本不會觸發搜尋阿XD)

    query_parts = []

    temp_cleaned_keyword = re.sub(r"[^a-zA-Z0-9 ]", "", payload.keyword)
    cleaned = "".join(map(lambda x: f"%{x}%" if x else x, temp_cleaned_keyword.strip().split()))

    if cleaned:
        query_parts.append(
            f"(@name:({cleaned})) => {{'$weight': 5.0;}} | (@description:({cleaned}))"
        )

    if payload.price:
        min_, max_ = get_price_range(payload.price).values()
        query_parts.append(f"(@price:[{min_} {max_}])")

    if payload.brands:
        if isinstance(payload.brands, list):
            brands = " | ".join(payload.brands)
        else:
            brands = payload.brands
        query_parts.append(f"(@brand:{{{brands}}})")

    if payload.categories:
        if isinstance(payload.categories, list):
            categories = " | ".join(payload.categories)
        else:
            categories = payload.categories
        query_parts.append(f"(@category:{{{categories}}})")

    query = " | ".join(query_parts)
    # 用|隔開的query

    # 添加sort or not
    if payload.sort_by and payload.order_by:
        sort_clause = f"SORTBY {payload.sort_by} {'DESC' if payload.order_by == 'desc' else 'asc'}"
        query += " " + sort_clause

    # 加上limit
    offset = (payload.page - 1) * payload.limit
    limit_clause = f"LIMIT {offset} {payload.limit}"
    query += " " + limit_clause

    print(query, "這是query")

    # total, document = await redis.execute_command("FT.SEARCH", products_index_key(), query)
    query = "@title:hello @price:[0 100] @tags:{ foo bar | hello world }"
    command = f"FT.SEARCH {products_index_key()} '{query}'"
    print(command, "")
    res = redis.execute_command(
        'FT.SEARCH idx "@title:hello @price:[0 100] @tags:{ foo bar | hello world }'
    )
    # res = redis.execute_command(
    #     "FT.SEARCH",
    #     products_index_key(),
    #     "@title:hello",
    #     "@price:[0 100]",
    #     "@tags:{foo bar | hello world}",
    # )

    print(res, "這是res")

    # print(res.total, "這是total!")
    # print(res.documents, "這是doc!")
    # return {
    #     "total": total,
    #     "list": map(lambda x: deserialize(x["id"].replace("products#", ""), x["value"]), document),
    # }
