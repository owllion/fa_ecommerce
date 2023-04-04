from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import uvicorn

from .routers import index
#from .models import item_model,user_model
#from .database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=index.router, prefix="/api")

#db.Base.metadata.create_all(db.engine)
# item_model.Base.metadata.create_all(db.engine)
# user_model.Base.metadata.create_all(db.engine)

@app.get("/")
def go_to_doc():
    return RedirectResponse(url="/docs/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)