from typing import Type

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from ..schemas.router_schema import RouterSettingParamsSchema
from ..utils.dependencies import validate_token


def get_router_settings(params: RouterSettingParamsSchema ) -> dict:
    is_protected,prefix,tags,responses = params.values()

    if is_protected:
        dependencies = [Depends(validate_token)]
        return {
            "prefix": prefix, 
            "tags": tags, 
            "dependencies": dependencies,
            "responses": responses
        }
    
    return {
        "prefix": prefix, 
        "tags": tags, 
        "responses": responses
    }

def get_path_decorator_settings(description: str,response_model: Type[BaseModel] = None):
    return {
        'status_code': status.HTTP_200_OK,
        'response_description': description,
        'response_model': response_model
    }