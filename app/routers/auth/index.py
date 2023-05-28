from fastapi import APIRouter

from . import auth_router as auth
from . import github_login_router as github
from . import google_login_router as google

auth_router = APIRouter()
google_router = APIRouter()
github_router = APIRouter()

auth_router.include_router(auth.public_singular)
google_router.include_router(google.router)
github_router.include_router(github.router)
