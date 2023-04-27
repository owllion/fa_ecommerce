from pydantic import BaseModel


class SocialLoginSchema(BaseModel):
    reqUrl: str