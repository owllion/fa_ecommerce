from fastapi import APIRouter

from . import auth_router, coupon_router, product_router, review_router, user_router

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

#reivew
router.include_router(review_router.protected_plural)
router.include_router(review_router.protected_singular)
router.include_router(review_router.public_plural)
router.include_router(review_router.public_singular)

#cart

#order

#coupon
router.include_router(coupon_router.protected_plural)
router.include_router(coupon_router.protected_singular)
router.include_router(coupon_router.public_plural)
router.include_router(coupon_router.public_singular)



