from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0"
)


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