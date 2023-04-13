from typing import Dict, List

from pydantic import BaseModel


class RouterSettingParamsSchema(BaseModel):
    singular_prefix: str
    plural_prefix: str
    tags: List[str]
    # responses: Dict[int, Dict[str, str]]