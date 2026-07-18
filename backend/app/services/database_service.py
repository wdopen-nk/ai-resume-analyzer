import json

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.analysis import Analysis
from app.models.resume import Resume


class DatabaseService:

    @staticmethod
    def save_analysis(
        filename: str,
        resume_text: str,
        analysis: dict
    ) -> int:

        db: Session = SessionLocal()

        try:
            resume = Resume(
                filename=filename,
                content=resume_text
            )

            db.add(resume)
            db.commit()
            db.refresh(resume)

            analysis_model = Analysis(
                resume_id=resume.id,
                resume_score=analysis["resume_score"],
                ats_score=analysis["ats_score"],
                strengths=json.dumps(analysis["strengths"]),
                weaknesses=json.dumps(analysis["weaknesses"]),
                missing_skills=json.dumps(analysis["missing_skills"]),
                recommendations=json.dumps(analysis["recommendations"]),
            )

            db.add(analysis_model)
            db.commit()

            return resume.id

        finally:
            db.close()

    @staticmethod
    def get_history():

        db = SessionLocal()

        try:
            resumes = (
                db.query(Resume)
                .order_by(Resume.uploaded_at.desc())
                .all()
            )

            history = []

            for resume in resumes:

                analysis = (
                    db.query(Analysis)
                    .filter(Analysis.resume_id == resume.id)
                    .first()
                )

                history.append({
                    "id": resume.id,
                    "filename": resume.filename,
                    "uploaded_at": resume.uploaded_at,
                    "resume_score": analysis.resume_score,
                    "ats_score": analysis.ats_score
                })

            return history

        finally:
            db.close()

    
    @staticmethod
    def get_analysis(resume_id: int):

        db = SessionLocal()

        try:

            resume = (
                db.query(Resume)
                .filter(Resume.id == resume_id)
                .first()
            )

            if resume is None:
                return None

            analysis = (
                db.query(Analysis)
                .filter(Analysis.resume_id == resume.id)
                .first()
            )

            if analysis is None:
                return None

            return {
                "id": resume.id,
                "filename": resume.filename,
                "uploaded_at": resume.uploaded_at,

                "resume_score": analysis.resume_score,
                "ats_score": analysis.ats_score,

                "strengths": json.loads(analysis.strengths),
                "weaknesses": json.loads(analysis.weaknesses),
                "missing_skills": json.loads(analysis.missing_skills),
                "recommendations": json.loads(analysis.recommendations),
            }

        finally:
            db.close()