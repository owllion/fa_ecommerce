from fastapi import APIRouter

from . import auth_router as auth

auth_router = APIRouter()
auth_router.include_router(auth.router)





