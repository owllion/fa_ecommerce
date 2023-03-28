from fastapi import Depends, FastAPI

from .utils.dependencies import get_query_token

from .routers import items,user
import uvicorn

app = FastAPI()
app.include_router(items.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)