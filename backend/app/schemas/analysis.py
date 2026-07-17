from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    resume_score: int
    ats_score: int
    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]
    recommendations: list[str]