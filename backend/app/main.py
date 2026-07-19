from fastapi import FastAPI

from app.api.resume import router as resume_router
from app.config import settings
from app.database.init_db import init_db
from app.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

init_db()

logger.info("Database initialized.")

app.include_router(resume_router)


@app.get("/")
def root():
    logger.info("Health check requested.")

    return {
        "message": f"{settings.APP_NAME} API is running."
    }