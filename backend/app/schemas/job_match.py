from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):

    resume_id: int = Field(
        ...,
        gt=0
    )

    job_title: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    job_description: str = Field(
        ...,
        min_length=20
    )


class JobMatchResponse(BaseModel):

    id: int | None = None

    resume_id: int

    job_title: str
    job_description: str

    match_score: int = Field(
        ...,
        ge=0,
        le=100
    )

    skills_match: int = Field(
        ...,
        ge=0,
        le=100
    )

    experience_match: int = Field(
        ...,
        ge=0,
        le=100
    )

    keyword_match: int = Field(
        ...,
        ge=0,
        le=100
    )

    matching_skills: list[str]
    missing_skills: list[str]

    matching_keywords: list[str]
    missing_keywords: list[str]

    recommendations: list[str]