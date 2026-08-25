from datetime import datetime

from sqlalchemy import String, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_title = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)

    match_score = Column(Integer, nullable=False)
    skills_match = Column(Integer, nullable=False)
    experience_match = Column(Integer, nullable=False)
    keyword_match = Column(Integer, nullable=False)

    matching_skills = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)

    matching_keywords = Column(Text, nullable=True)
    missing_keywords = Column(Text, nullable=True)

    recommendations = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    resume = relationship("Resume", back_populates="job_matches")