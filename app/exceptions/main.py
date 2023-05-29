from authlib.integrations.starlette_client import OAuthError
from fastapi import HTTPException, status

from ..constants.api_msgs import SERVER_ERROR


class CustomHTTPException(HTTPException):
    def __init__(self, detail: str = "An error occurred."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


# for service's functions
def raise_http_exception(detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    raise HTTPException(status_code=status_code, detail=detail)


# for api endpoint try/except
def get_exception(e: Exception):
    if isinstance(e, (HTTPException,)):
        raise e
    raise CustomHTTPException(detail=str(e))


# for social login, i.g google,github login
def get_social_login_exception(e: Exception):
    if isinstance(e, (HTTPException,)):
        raise e

    if isinstance(e, (OAuthError,)):
        raise_http_exception(detail=e.description, status_code=status.HTTP_401_UNAUTHORIZED)

    raise_http_exception(str(e))
