import aioredis


async def redis_pool(db: int = 0):
    """
    redis连接池
    :return:
    """
    redis = await aioredis.create_redis_pool(
        f"redis://:{redis_config.get('password')}@{redis_config.get('host')}/{db}?encoding=utf-8"
    )
    return redis


def create_app():
    application = FastAPI()
    application.include_router(api_router, prefix="/api")
    application.include_router(wss_router, prefix="/ws")
    return application


app = create_app()


@app.on_event("startup")
async def create_redis():
    app.state.redis = await redis_pool()


@app.on_event("shutdown")
async def close_redis():
    await app.state.redis.close()
