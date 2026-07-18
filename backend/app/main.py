from fastapi import FastAPI

from app.database.init_db import init_db
from app.api.resume import router as resume_router

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0"
)

init_db()

app.include_router(resume_router)

@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }