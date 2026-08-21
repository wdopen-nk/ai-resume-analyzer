from pydantic import BaseModel, Field

class JobMatchRequest(BaseModel):
    resume_id: int = Field(..., gt=0)
    job_description: str = Field(..., min_length=20)