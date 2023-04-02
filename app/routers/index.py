from fastapi import APIRouter
from ..routers import auth_router,user_router,product_router

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(user_router.router)
router.include_router(product_router.public_router)
