import json

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.analysis import Analysis
from app.models.resume import Resume
from app.models.job_match import JobMatch
from app.models.user import User


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
                skills_score=analysis["skills_score"],
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
                    "ats_score": analysis.ats_score,
                    "skills_score": analysis.skills_score,
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
                "skills_score": analysis.skills_score,

                "strengths": json.loads(analysis.strengths),
                "weaknesses": json.loads(analysis.weaknesses),
                "missing_skills": json.loads(analysis.missing_skills),
                "recommendations": json.loads(analysis.recommendations),
            }

        finally:
            db.close()


    @staticmethod
    def delete_resume(resume_id: int) -> bool:

        db = SessionLocal()

        try:

            resume = (
                db.query(Resume)
                .filter(Resume.id == resume_id)
                .first()
            )

            if resume is None:
                return False

            analysis = (
                db.query(Analysis)
                .filter(Analysis.resume_id == resume_id)
                .first()
            )

            if analysis:
                db.delete(analysis)

            db.delete(resume)

            db.commit()

            return True

        finally:
            db.close()


    @staticmethod
    def get_resume(resume_id: int):
        db = SessionLocal()

        try:
            return db.query(Resume).filter(
                Resume.id == resume_id
            ).first()
        finally:
            db.close()


    @staticmethod
    def save_job_match(
        resume_id: int,
        job_title: str,
        job_description: str,
        result: dict
    ) -> int:

        db = SessionLocal()

        try:

            job_match = JobMatch(
                resume_id=resume_id,
                job_title=job_title,
                job_description=job_description,

                match_score=result["match_score"],
                skills_match=result["skills_match"],
                experience_match=result["experience_match"],
                keyword_match=result["keyword_match"],

                matching_skills=json.dumps(
                    result["matching_skills"]
                ),
                missing_skills=json.dumps(
                    result["missing_skills"]
                ),

                matching_keywords=json.dumps(
                    result["matching_keywords"]
                ),
                missing_keywords=json.dumps(
                    result["missing_keywords"]
                ),

                recommendations=json.dumps(
                    result["recommendations"]
                )
            )

            db.add(job_match)
            db.commit()
            db.refresh(job_match)

            return job_match.id

        finally:
            db.close()


    @staticmethod
    def get_job_matches(resume_id: int):

        db = SessionLocal()

        try:

            matches = (
                db.query(JobMatch)
                .filter(JobMatch.resume_id == resume_id)
                .order_by(JobMatch.created_at.desc())
                .all()
            )

            return [
                {
                    "id": match.id,
                    "resume_id": match.resume_id,
                    "job_title": match.job_title,
                    "job_description": match.job_description,

                    "match_score": match.match_score,
                    "skills_match": match.skills_match,
                    "experience_match": match.experience_match,
                    "keyword_match": match.keyword_match,

                    "matching_skills": json.loads(
                        match.matching_skills
                    ),

                    "missing_skills": json.loads(
                        match.missing_skills
                    ),

                    "matching_keywords": json.loads(
                        match.matching_keywords
                    ),

                    "missing_keywords": json.loads(
                        match.missing_keywords
                    ),

                    "recommendations": json.loads(
                        match.recommendations
                    ),

                    "created_at": match.created_at,
                }
                for match in matches
            ]

        finally:
            db.close()


    @staticmethod
    def get_user_by_email(email: str):

        db = SessionLocal()

        try:
            return (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

        finally:
            db.close()


    @staticmethod
    def create_user(
        email: str,
        password_hash: str
    ) -> User:

        db = SessionLocal()

        try:

            user = User(
                email = email,
                password_hash = password_hash
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return user

        finally:
            db.close()
