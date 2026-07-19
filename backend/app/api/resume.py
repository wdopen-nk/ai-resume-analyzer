import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.parser_service import ResumeParser
from app.services.ai_service import AIService
from app.services.database_service import DatabaseService

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