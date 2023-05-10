from .....schemas.product_schema import ProductSchema


def serialize(product: ProductSchema):
    del product["id"]
    return {**product}
