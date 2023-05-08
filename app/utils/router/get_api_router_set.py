from fastapi import APIRouter

from .router_settings import get_router_settings


def get_api_router_set(singular_prefix: str, plural_prefix: str, tags: list[str]):
    return get_router_settings(singular_prefix, plural_prefix, tags)
