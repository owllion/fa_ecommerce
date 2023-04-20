from fastapi import APIRouter

from . import coupon_router as coupon

coupon_router = APIRouter()

coupon_router.include_router(coupon.protected_plural)
coupon_router.include_router(coupon.protected_singular)
coupon_router.include_router(coupon.public_plural)
coupon_router.include_router(coupon.public_singular)




