from fastapi import HTTPException,status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from decouple import config

from .set_template import set_template
from .get_mail_text import get_mail_text
from .get_html_template import get_html_template
from ...exceptions.http_exception import CustomHTTPException
from ...schemas import email_schema

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_FROM"),
    MAIL_PASSWORD = config("MAIL_PWD"),
    MAIL_FROM = config("MAIL_PWD"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_link(params: email_schema.SendLinkParamsSchema):

    link_type,link,email = params.values()

    (
        btn_text,
        title,
        content,
        link_type,
        action,
    ) = get_mail_text(link_type);

    try:
        message = MessageSchema(
            subject= title,
            recipients= email,
            body= set_template({
                "btnText": btn_text,
                "btnLink": link,
                "title": title,
                "content": content,
                "link_type": link_type,
                "action": action
            }),
            subtype=MessageType.html
            #default-> text,if it's not,then must set this property.
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        raise CustomHTTPException(detail= str(e))