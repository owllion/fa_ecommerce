from fastapi import APIRouter, Depends
from ..utils.dependencies import validate_token
from ..schemas.router_schema import RouterSettingParamsSchema

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

