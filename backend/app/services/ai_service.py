import json

from ollama import chat

from app.services.prompt_service import PromptService
from app.config import settings


class AIService:
    """Communicates with the Ollama model."""

    MODEL = settings.OLLAMA_MODEL  # Change if using another model

    @classmethod
    def analyze_resume(cls, resume_text: str) -> dict:
        prompt = PromptService.resume_prompt(resume_text)

        response = chat(
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