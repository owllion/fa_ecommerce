from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, detail: str = "An error occurred."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


# for api endpoint try/except
def get_exception(e: Exception):
    if isinstance(e, (HTTPException,)):
        raise e
    raise CustomHTTPException(detail=str(e))


# for service's functions
def raise_http_exception(detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    raise HTTPException(status_code=status_code, detail=detail)
