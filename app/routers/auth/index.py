from fastapi import APIRouter

from . import auth_router as auth
from . import fb_login_router as fb
from . import github_login_router as github
from . import google_login_router as google

auth_router = APIRouter()
google_router = APIRouter()
github_router = APIRouter()
fb_router = APIRouter()

auth_router.include_router(auth.router)
google_router.include_router(google.router)
github_router.include_router(github.router)
fb_router.include_router(fb.router)





