from fastapi import HTTPException, status


def raise_http_exception(detail: str,status_code: int = status.HTTP_400_BAD_REQUEST):
    raise HTTPException(
        status_code= status_code,
        detail= detail
    )