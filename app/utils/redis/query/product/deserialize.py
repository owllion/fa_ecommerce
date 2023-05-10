from .....schemas.product_schema import ProductSchema


def deserialize(product_id: str, product: ProductSchema):
    return {**product, "id": product_id}
