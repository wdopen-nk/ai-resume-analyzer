from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    resume_score: int
    ats_score: int

    experience_score: int
    education_score: int
    skills_score: int

    summary: str

    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]
    recommendations: list[str]