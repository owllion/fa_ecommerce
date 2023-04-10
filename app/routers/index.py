from fastapi import APIRouter

from ..routers import auth_router, product_router, user_router

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(user_router.protected_router)
router.include_router(user_router.public_router)
router.include_router(product_router.public_router)
router.include_router(product_router.protected_router)
