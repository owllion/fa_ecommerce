# create index for product list searching
import aioredis
import redis
from redis.commands.search.field import NumericField, TagField, TextField

from .keys import products_index_key


def create_product_index(client: redis.Redis):
    # 先判斷index是否已經存在
    indexes = client.execute_command("FT._LIST")
    print(list(indexes), "這是已經創建的index列表")
    print(client.ft(products_index_key()).info(), "product index 詳情")
    if products_index_key() in indexes:
        return
    # price brand category
    schema = (
        TextField("product_name", weight=5.0, sortable=True),
        TextField(
            "description",
        ),
        NumericField("price", sortable=True),
        TagField(
            "brand",
        ),
        TagField(
            "category",
        ),
        NumericField("created_at", sortable=True),
    )

    # await client.execute_command("FT.CREATE", products_index_key(), schema)

    schema = "SCHEMA product_name TEXT SORTABLE description TEXT price NUMERIC SORTABLE created_at NUMERIC SORTABLE brand TAG category TAG"

    command = f"FT.CREATE {products_index_key()} ON HASH PREFIX 1 products# {schema}"

    client.execute_command(command)

    print(client.ft(products_index_key()).info(), "product index 詳情")
