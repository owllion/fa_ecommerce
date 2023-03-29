from fastapi import Depends, FastAPI

from .routers import items,user
from .database import db
from .models import item as item_model,user as user_model
import uvicorn

app = FastAPI()

app.include_router(items.router)
app.include_router(user.router)

item_model.Base.metadata.create_all(db.engine)
user_model.Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)