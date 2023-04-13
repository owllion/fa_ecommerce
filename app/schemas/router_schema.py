from typing import Dict, List

from pydantic import BaseModel


class RouterSettingParamsSchema(BaseModel):
    is_protected: bool
    prefix: str
    tags: List[str]
    responses: Dict[int, Dict[str, str]]