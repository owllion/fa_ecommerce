import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from .routers import index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#We need this SessionMiddleware, because Authlib will use request.session to store temporary codes and states.
app.add_middleware(SessionMiddleware, secret_key=config("SESSION_MIDDLEWARE_SECRET"))

app.include_router(router=index.router, prefix="/api")


@app.get("/")
def go_to_doc():
    return RedirectResponse(url="/docs/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)