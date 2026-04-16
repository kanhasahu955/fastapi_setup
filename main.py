import uvicorn
import logging
from fastapi import FastAPI,Request
from contextlib import asynccontextmanager
from time import time

from app.core.env import get_settings
from app.core.db import init_db,close_db
from app.core.cors import setup_cors
from app.api.routes import router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


settings = get_settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info('connecting to the database...')
    await init_db()
    logger.info('database connected successfully')
    yield
    logger.info('closing database connection.. ')
    await close_db()
    logger.info('closing connection closed')

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    logger.info(f"REQUEST -> {request.method} {request.url}")
    response = await call_next(request)
    duration = round(time() - start_time, 3)
    logger.info(
        f"RESPONSE -> status={response.status_code} duration={duration}s"
    )
    return response

setup_cors(app)
app.include_router(router,prefix='/api/v1')


if __name__ == '__main__':
    logger.info("Server starting at http://localhost:4000")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=4000,
        reload=True,
        log_level="info"
    )

