import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from .routers import index

app = FastAPI()
ALLOWED_HOSTS = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=index.router, prefix="/api")


@app.get("/")
def go_to_doc():
    return RedirectResponse(url="/docs/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4438, reload=True )
    # ssl_keyfile="./cert/key.pem", ssl_certfile="./cert/cert.pem"