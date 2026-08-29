import json

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.analysis import Analysis
from app.models.job_match import JobMatch
from app.models.resume import Resume
from app.models.user import User


class DatabaseService:

    @staticmethod
    def save_analysis(
        filename: str,
        resume_text: str,
        analysis: dict,
        user_id: int
    ) -> int:

        db: Session = SessionLocal()

        try:

            resume = Resume(
                filename=filename,
                content=resume_text,
                user_id=user_id
            )

            db.add(resume)

            # Generate resume.id without committing
            db.flush()

            analysis_model = Analysis(
                resume_id=resume.id,
                resume_score=analysis["resume_score"],
                ats_score=analysis["ats_score"],
                skills_score=analysis["skills_score"],
                strengths=json.dumps(
                    analysis["strengths"]
                ),
                weaknesses=json.dumps(
                    analysis["weaknesses"]
                ),
                missing_skills=json.dumps(
                    analysis["missing_skills"]
                ),
                recommendations=json.dumps(
                    analysis["recommendations"]
                ),
            )

            db.add(analysis_model)

            # Commit Resume + Analysis together
            db.commit()

            return resume.id

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()


    @staticmethod
    def get_history(user_id: int):

        db: Session = SessionLocal()

        try:

            resumes = (
                db.query(Resume)
                .filter(
                    Resume.user_id == user_id
                )
                .order_by(
                    Resume.uploaded_at.desc()
                )
                .all()
            )

            history = []

            for resume in resumes:

                analysis = (
                    db.query(Analysis)
                    .filter(
                        Analysis.resume_id == resume.id
                    )
                    .first()
                )

                if analysis is None:
                    continue

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
    def get_analysis(
        resume_id: int,
        user_id: int
    ):

        db: Session = SessionLocal()

        try:

            # Verify that the resume belongs to the user
            resume = (
                db.query(Resume)
                .filter(
                    Resume.id == resume_id,
                    Resume.user_id == user_id
                )
                .first()
            )

            if resume is None:
                return None

            analysis = (
                db.query(Analysis)
                .filter(
                    Analysis.resume_id == resume.id
                )
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

                "strengths": json.loads(
                    analysis.strengths
                ),

                "weaknesses": json.loads(
                    analysis.weaknesses
                ),

                "missing_skills": json.loads(
                    analysis.missing_skills
                ),

                "recommendations": json.loads(
                    analysis.recommendations
                ),
            }

        finally:

            db.close()


    @staticmethod
    def delete_resume(
        resume_id: int,
        user_id: int
    ) -> bool:

        db: Session = SessionLocal()

        try:

            # Only find the resume if it belongs
            # to the authenticated user.
            resume = (
                db.query(Resume)
                .filter(
                    Resume.id == resume_id,
                    Resume.user_id == user_id
                )
                .first()
            )

            if resume is None:
                return False

            # Delete the analysis associated
            # with the resume.
            analysis = (
                db.query(Analysis)
                .filter(
                    Analysis.resume_id == resume_id
                )
                .first()
            )

            if analysis:
                db.delete(analysis)

            # Job matches are configured with
            # ON DELETE CASCADE.
            db.delete(resume)

            db.commit()

            return True

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()


    @staticmethod
    def get_resume(
        resume_id: int,
        user_id: int
    ):

        db: Session = SessionLocal()

        try:

            return (
                db.query(Resume)
                .filter(
                    Resume.id == resume_id,
                    Resume.user_id == user_id
                )
                .first()
            )

        finally:

            db.close()


    @staticmethod
    def save_job_match(
        resume_id: int,
        job_title: str,
        job_description: str,
        result: dict
    ) -> int:

        db: Session = SessionLocal()

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

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()


    @staticmethod
    def get_job_matches(
        resume_id: int,
        user_id: int
    ):

        db: Session = SessionLocal()

        try:

            matches = (
                db.query(JobMatch)
                .join(
                    Resume,
                    JobMatch.resume_id == Resume.id
                )
                .filter(
                    JobMatch.resume_id == resume_id,
                    Resume.user_id == user_id
                )
                .order_by(
                    JobMatch.created_at.desc()
                )
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
    def get_user_by_email(
        email: str
    ):

        db: Session = SessionLocal()

        try:

            return (
                db.query(User)
                .filter(
                    User.email == email
                )
                .first()
            )

        finally:

            db.close()


    @staticmethod
    def create_user(
        email: str,
        password_hash: str
    ) -> User:

        db: Session = SessionLocal()

        try:

            user = User(
                email=email,
                password_hash=password_hash
            )

            db.add(user)

            db.commit()
            db.refresh(user)

            return user

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()


    @staticmethod
    def get_user_by_id(
        user_id: int
    ):

        db: Session = SessionLocal()

        try:

            return (
                db.query(User)
                .filter(
                    User.id == user_id
                )
                .first()
            )

        finally:

            db.close()
