from pydantic import BaseModel


class ResumeResponse(BaseModel):
    filename: str
    text: str