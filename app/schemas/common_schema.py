from pydantic import BaseModel

"""
common schema file to avoid circular import.
"""
class ProductInfoInCartSchema(BaseModel):
    thumbnail: str
    product_name: str
    class Config:
        orm_mode = True
