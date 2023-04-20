from fastapi import APIRouter

from .auth.index import auth_router
from .coupon.index import coupon_router
from .order.index import order_item_router, order_router
from .product.index import product_item_router, product_router
from .review.index import review_router
from .user.index import user_fav_router, user_router

router = APIRouter()

#auth
router.include_router(auth_router)

#user
router.include_router(user_router)
router.include_router(user_fav_router)

#product
router.include_router(product_router)
router.include_router(product_item_router)

#reivew
router.include_router(review_router)

#order
router.include_router(order_router)
router.include_router(order_item_router)

#coupon
router.include_router(coupon_router)




