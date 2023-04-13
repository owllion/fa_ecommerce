from typing import Type

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from ..constants import api_msgs
from ..schemas.router_schema import RouterSettingParamsSchema
from ..utils.dependencies import validate_token


def get_api_route_config(
    prefix: str, 
    tags: list[str], 
    is_protected: bool
):

    res = {
        "prefix": f'/{prefix}',
        "tags": tags,
        "responses": api_msgs.API_RESPONSES 
    }

    if is_protected:
        res['dependencies'] = [Depends(validate_token)] 

    return res


def get_router_settings(
    singular_prefix: str, 
    plural_prefix: str,
    tags: list[str]
) -> dict:
    
    protected_singular = APIRouter(
        **get_api_route_config(
            prefix=singular_prefix,
            tags=tags,
            is_protected= True
        )
    )

    protected_plural = APIRouter(
        **get_api_route_config(
            prefix= plural_prefix,
            tags= tags,
            is_protected= True
        )
    )


    public_singular = APIRouter(
        **get_api_route_config(
            prefix= singular_prefix,
            tags= tags,
            is_protected= False
        )
    )
    public_plural = APIRouter(
        **get_api_route_config(
            prefix= plural_prefix,
            tags= tags,
            is_protected= False
        )
    )

    return (
        protected_plural,
        protected_singular,
        public_plural,
        public_singular
    )



def get_path_decorator_settings(description: str,response_model: Type[BaseModel] = None):
    return {
        'status_code': status.HTTP_200_OK,
        'response_description': description,
        'response_model': response_model
    }