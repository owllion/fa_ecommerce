from fastapi.encoders import jsonable_encoder

from .....schemas.product_schema import ProductSchema


def serialize(product: ProductSchema):
    product_dict = jsonable_encoder(product)
    del product_dict["id"]
    return product_dict
