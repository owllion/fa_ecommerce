from decouple import config
from fastapi import HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from ...exceptions.custom_http_exception import CustomHTTPException
from ...schemas import email_schema
from .get_mail_text import get_mail_text
from .set_template import set_template

conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_FROM"),
    MAIL_PASSWORD=config("MAIL_PWD"),
    MAIL_FROM=config("MAIL_FROM", cast=str),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_link(params: email_schema.SendLinkParamsSchema):
    link_type, link, email = params.values()

    res = get_mail_text(link_type)
    print(res, "this is res")
    btn_text, title, content, link_type, action = get_mail_text(link_type).values()

    try:
        message = MessageSchema(
            subject=title,
            recipients=[email],
            body=set_template(
                {
                    "btnText": btn_text,
                    "btnLink": link,
                    "title": title,
                    "content": content,
                    "link_type": link_type,
                    "action": action,
                }
            ),
            subtype=MessageType.html
            # default-> text,if it's not,then must set this property.
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        print("await after@")

    except Exception as e:
        raise CustomHTTPException(detail=str(e))
