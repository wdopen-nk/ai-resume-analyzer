import shutil
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from app.services.parser_service import ResumeParser
from app.services.ai_service import AIService
from app.services.database_service import DatabaseService
from app.schemas.job_match import JobMatchRequest, JobMatchResponse
from app.services.job_match_service import JobMatchService

from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


UPLOAD_FOLDER = Path("app/uploads")
UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


CurrentUser = Annotated[
    User,
    Depends(get_current_user)
]


@router.post("/upload")
async def upload_resume(
    current_user: CurrentUser,
    file: UploadFile = File(...)
):
    extension = Path(file.filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # Generate a unique temporary filename.
    # The original filename is still stored in the database.
    temporary_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = UPLOAD_FOLDER / temporary_filename

    try:
        # Save uploaded file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Release the uploaded file handle.
        # This is especially important on Windows.
        await file.close()

        # Extract text
        resume_text = ResumeParser.extract_text(
            str(file_path)
        )

        # Analyze resume
        analysis = AIService.analyze_resume(
            resume_text
        )

        # Save resume and analysis
        # associated with the authenticated user.
        resume_id = DatabaseService.save_analysis(
            filename=file.filename,
            resume_text=resume_text,
            analysis=analysis,
            user_id=current_user.id
        )

        return {
            "id": resume_id,
            "filename": file.filename,
            "analysis": analysis
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while analyzing the resume."
        )

    finally:
        # Always remove the temporary file.
        if file_path.exists():
            try:
                file_path.unlink()
            except PermissionError:
                # Avoid masking the original error if Windows
                # still has the file temporarily locked.
                pass


@router.get("/history")
def get_history(
    current_user: CurrentUser
):

    return DatabaseService.get_history(
        current_user.id
    )


@router.get("/{resume_id}")
def get_resume_analysis(
    resume_id: int,
    current_user: CurrentUser
):

    analysis = DatabaseService.get_analysis(
        resume_id,
        current_user.id
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Resume analysis not found."
        )

    return analysis


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    current_user: CurrentUser
):

    deleted = DatabaseService.delete_resume(
        resume_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    return {
        "message": "Resume deleted successfully."
    }


@router.post(
    "/match",
    response_model=JobMatchResponse
)
def match_resume(
    request: JobMatchRequest,
    current_user: CurrentUser
):

    resume = DatabaseService.get_resume(
        request.resume_id,
        current_user.id
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    try:

        result = JobMatchService.match_resume(
            resume.content,
            request.job_description
        )

        job_match_id = DatabaseService.save_job_match(
            resume_id=request.resume_id,
            job_title=request.job_title,
            job_description=request.job_description,
            result=result,
            user_id=current_user.id
        )

        return {
            "id": job_match_id,
            "resume_id": request.resume_id,
            "job_title": request.job_title,
            "job_description": request.job_description,
            **result
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while matching the resume."
        )


@router.get("/{resume_id}/matches")
def get_job_matches(
    resume_id: int,
    current_user: CurrentUser
):

    resume = DatabaseService.get_resume(
        resume_id,
        current_user.id
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    return DatabaseService.get_job_matches(
        resume_id,
        current_user.id
    )