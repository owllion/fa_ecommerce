from fastapi.encoders import jsonable_encoder

from .....schemas.product_schema import ProductSchema


def deserialize(product: ProductSchema):
    return jsonable_encoder(product)
