from fastapi import APIRouter

from ..routers import auth_router, product_router, review_router, user_router
from .api_router_settings import protected_plural as review_protected_plural
from .api_router_settings import protected_singular as review_protected_singular
from .api_router_settings import public_plural as review_public_plural
from .api_router_settings import public_singular as review_public_singular

router = APIRouter()

router.include_router(auth_router.router)

router.include_router(user_router.public_router)
router.include_router(user_router.protected_router)

router.include_router(product_router.public_router)
router.include_router(product_router.protected_router)

router.include_router(review_protected_plural)
router.include_router(review_protected_singular)
router.include_router(review_public_plural)
router.include_router(review_protected_singular)


