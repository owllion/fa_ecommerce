from fastapi import HTTPException, status

class CustomHTTPException(HTTPException):
    def __init__(self, detail: str = 'An error occurred.'):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
