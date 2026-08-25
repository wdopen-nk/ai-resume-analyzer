import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.parser_service import ResumeParser
from app.services.ai_service import AIService
from app.services.database_service import DatabaseService
from app.schemas.job_match import JobMatchRequest, JobMatchResponse
from app.services.job_match_service import JobMatchService

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_FOLDER = Path("app/uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    file_path = UPLOAD_FOLDER / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resume_text = ResumeParser.extract_text(str(file_path))

        analysis = AIService.analyze_resume(resume_text)

        resume_id = DatabaseService.save_analysis(
            filename=file.filename,
            resume_text=resume_text,
            analysis=analysis
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while analyzing the resume.",
        )

    # except Exception as e:
    #     print("ERROR DURING RESUME ANALYSIS:")
    #     print(repr(e))
    #     raise HTTPException(
    #         status_code=500,
    #         detail=str(e)
    #     )
    
    return {
        "id": resume_id,
        "filename": file.filename,
        "analysis": analysis
    }


@router.get("/history")
def get_history():
    return DatabaseService.get_history()


@router.get("/{resume_id}")
def get_resume_analysis(resume_id: int):

    analysis = DatabaseService.get_analysis(resume_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Resume analysis not found."
        )

    return analysis


@router.delete("/{resume_id}")
def delete_resume(resume_id: int):

    deleted = DatabaseService.delete_resume(resume_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    return {
        "message": "Resume deleted successfully."
    }


@router.post("/match", response_model=JobMatchResponse)
def match_resume(request: JobMatchRequest):

    resume = DatabaseService.get_resume(
        request.resume_id
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

        print("JOB MATCH RESULT:")
        print(result)

        job_match_id = DatabaseService.save_job_match(
            resume_id=request.resume_id,
            job_title=request.job_title,
            job_description=request.job_description,
            result=result
        )

        return {
            "id": job_match_id,
            "resume_id": request.resume_id,
            "job_title": request.job_title,
            "job_description": request.job_description,
            **result
        }

    except ValueError as e:

        print("JOB MATCH VALUE ERROR:")
        print(repr(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        print("JOB MATCH ERROR:")
        print(repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{resume_id}/matches")
def get_job_matches(resume_id: int):

    resume = DatabaseService.get_resume(
        resume_id
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    return DatabaseService.get_job_matches(
        resume_id
    )