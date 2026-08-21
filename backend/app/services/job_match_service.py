import json

from ollama import Client
from app.config import settings


class JobMatchService:
    """Compares a resume against a job description using Ollama."""

    MODEL = settings.OLLAMA_MODEL

    # Connect from Docker container -> Windows host
    client = Client(
        host="http://host.docker.internal:11434"
    )

    PROMPT_PATH = (
        "app/prompts/job_match_prompt.txt"
    )

    @classmethod
    def _load_prompt(cls) -> str:
        with open(
            cls.PROMPT_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()

    @classmethod
    def match_resume(
        cls,
        resume_text: str,
        job_description: str
    ) -> dict:

        prompt_template = cls._load_prompt()

        prompt = prompt_template.format(
            resume_text=resume_text,
            job_description=job_description
        )

        response = cls.client.chat(
            model=cls.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format="json",
        )

        return json.loads(response.message.content)