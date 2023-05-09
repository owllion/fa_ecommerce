# create index for product list searching
import aioredis
from redis.commands.search.field import TextField

from ..redis.keys import products_index_key


def create_product_key(client: aioredis.Redis):
    # 先判斷index是否已經存在
    indexes = client.execute_command("FT._LIST")
    print(indexes, "這是已經創建的index列表")
    exists = indexes.index(products_index_key())
    if exists:
        return
    # price brand category
    schema = (
        TextField("product_name", weight=5.0),
        TextField("description"),
    )
    client.ft(products_index_key()).create_index(schema)

    print(client.ft(products_index_key()).info(), "product index 詳情")
