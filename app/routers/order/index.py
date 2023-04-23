from fastapi import APIRouter

from . import line_pay_router as line_pay
from . import order_item_router as order_item
from . import order_router as order

order_router = APIRouter()
order_item_router = APIRouter()
line_pay_router = APIRouter()

#order
order_router.include_router(order.protected_plural)
order_router.include_router(order.protected_singular)
order_router.include_router(order.public_plural)
order_router.include_router(order.public_singular)

#order_item
order_item_router.include_router(order_item.protected_plural)
order_item_router.include_router(order_item.protected_singular)
order_item_router.include_router(order_item.public_plural)
order_item_router.include_router(order_item.public_singular)

#line_pay
line_pay_router.include_router(line_pay.protected_singular)
line_pay_router.include_router(line_pay.public_singular)

