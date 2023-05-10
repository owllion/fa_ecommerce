# create index for product list searching
import aioredis
from redis.commands.search.field import TextField

from .keys import products_index_key


async def create_product_index(client: aioredis.Redis):
    # 先判斷index是否已經存在
    indexes = await client.execute_command("FT._LIST")
    print(list(indexes), "這是已經創建的index列表")

    if products_index_key() in indexes:
        return
    # price brand category
    schema = (
        TextField("product_name", weight=5.0),
        TextField("description"),
    )
    # client.ft(products_index_key()).create_index(schema)

    # print(client.ft(products_index_key()).info(), "product index 詳情")
