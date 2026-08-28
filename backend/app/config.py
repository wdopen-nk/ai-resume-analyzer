import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "AI Resume Analyzer")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///resume_analyzer.db"
    )

    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434/api/generate"
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5:7b"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "your-super-secret-key-change-this"
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "60"
        )
    )


settings = Settings()