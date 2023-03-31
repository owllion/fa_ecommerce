from fastapi import Depends, FastAPI

from .routers import item_router,user_router,auth_router
from .models import item_model,user_model
from .database import db
import uvicorn

app = FastAPI()

app.include_router(item_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)

item_model.Base.metadata.create_all(db.engine)
user_model.Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)