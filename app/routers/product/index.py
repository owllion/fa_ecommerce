from fastapi import APIRouter

from . import product_item_router as product_item
from . import product_router as product

product_router = APIRouter()
product_item_router = APIRouter()

#product
product_router.include_router(product.protected_plural)
product_router.include_router(product.protected_singular)
product_router.include_router(product.public_plural)
product_router.include_router(product.public_singular)

#product_item
product_item_router.include_router(product_item.protected_plural)
product_item_router.include_router(product_item.protected_singular)
product_item_router.include_router(product_item.public_plural)
product_item_router.include_router(product_item.public_singular)



