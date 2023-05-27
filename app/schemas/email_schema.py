from pydantic import BaseModel


class CreateEmailContentSchema(BaseModel):
    btn_text: str
    btn_link: str
    title: str
    content: str
    link_type: str
    action: str


class SendLinkInfoBase(BaseModel):
    link_type: str
    email: str


class SendLinkSchema(SendLinkInfoBase):
    user_id: str
    url_params: str
    token_type: str


class SendLinkParamsSchema(SendLinkInfoBase):
    link: str
