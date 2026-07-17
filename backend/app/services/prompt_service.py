from pathlib import Path


class PromptService:
    """Loads and formats AI prompts."""

    PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

    @classmethod
    def resume_prompt(cls, resume_text: str) -> str:
        prompt_path = cls.PROMPTS_DIR / "resume_prompt.txt"

        prompt = prompt_path.read_text(encoding="utf-8")

        return prompt.replace("{{resume}}", resume_text)