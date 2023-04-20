from fastapi import APIRouter

from . import user_favorites_router as favorite
from . import user_router as user

user_router = APIRouter()
user_fav_router = APIRouter()

user_router.include_router(user.protected_singular)
user_router.include_router(user.public_singular)

user_fav_router.include_router(favorite.protected_singular)
user_fav_router.include_router(favorite.protected_plural)




