from fastapi import APIRouter

from . import review_router as review

review_router = APIRouter()

review_router.include_router(review.protected_plural)
review_router.include_router(review.protected_singular)
review_router.include_router(review.public_plural)
review_router.include_router(review.public_singular)




