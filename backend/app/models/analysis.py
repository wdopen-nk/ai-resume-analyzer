from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id")
    )

    resume_score: Mapped[int] = mapped_column(Integer)
    ats_score: Mapped[int] = mapped_column(Integer)
    skills_score: Mapped[int] = mapped_column(Integer)

    strengths: Mapped[str] = mapped_column(Text)
    weaknesses: Mapped[str] = mapped_column(Text)
    missing_skills: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[str] = mapped_column(Text)