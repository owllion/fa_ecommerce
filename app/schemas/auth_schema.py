from pydantic import BaseModel


class GithubLoginSchema(BaseModel):
    reqUrl: str