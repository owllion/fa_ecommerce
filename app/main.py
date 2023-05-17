import re

import aioredis
import redis
import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from .routers import index
from .utils.redis.create_index import create_product_index

# Make a regular expression
# for validating an Email
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


# Define a function for
# for validating an Email
def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        print("Valid Email")

    else:
        print("Invalid Email")


email = config("MAIL_FROM")

check(email)

app = FastAPI(title="React Ecommerce API")

# adaptor for running ASGI app in aws lambda
handler = Mangum(app)

ALLOWED_HOSTS = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=index.router, prefix="/api")


async def redis_pool():
    # redis = aioredis.Redis(
    #     host=config("REDIS_HOST"),
    #     port=config("REDIS_PORT"),
    #     password=config("REDIS_PW"),
    #     decode_responses=True,
    #     encoding="utf-8",
    # )
    myredis = redis.Redis(
        host=config("REDIS_HOST"),
        port=config("REDIS_PORT"),
        password=config("REDIS_PW"),
        decode_responses=True,
        encoding="utf-8",
    )

    return myredis


@app.on_event("startup")
async def create_redis():
    app.state.redis = await redis_pool()


@app.on_event("shutdown")
def close_redis():
    app.state.redis.close()


@app.get("/")
def go_to_doc():
    return RedirectResponse(url="/docs/")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        reload=True,
        ssl_keyfile="./cert/key.pem",
        ssl_certfile="./cert/cert.pem",
    )
