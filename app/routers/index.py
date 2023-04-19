from fastapi import APIRouter

from . import (
    auth_router,
    coupon_router,
    order_item_router,
    order_router,
    product_item_router,
    product_router,
    review_router,
    user_router,
)

router = APIRouter()

#auth
router.include_router(auth_router.router)

#user
router.include_router(user_router.protected_singular)
router.include_router(user_router.public_singular)

#product
router.include_router(product_router.protected_plural)
router.include_router(product_router.protected_singular)
router.include_router(product_router.public_plural)
router.include_router(product_router.public_singular)

#product_item
router.include_router(product_item_router.protected_plural)
router.include_router(product_item_router.protected_singular)
router.include_router(product_item_router.public_plural)
router.include_router(product_item_router.public_singular)

#reivew
router.include_router(review_router.protected_plural)
router.include_router(review_router.protected_singular)
router.include_router(review_router.public_plural)
router.include_router(review_router.public_singular)

#order
router.include_router(order_router.protected_plural)
router.include_router(order_router.protected_singular)
router.include_router(order_router.public_plural)
router.include_router(order_router.public_singular)

#order_item
router.include_router(order_item_router.protected_plural)
router.include_router(order_item_router.protected_singular)
router.include_router(order_item_router.public_plural)
router.include_router(order_item_router.public_singular)


#coupon
router.include_router(coupon_router.protected_plural)
router.include_router(coupon_router.protected_singular)
router.include_router(coupon_router.public_plural)
router.include_router(coupon_router.public_singular)



