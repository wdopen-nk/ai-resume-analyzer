from pathlib import Path
import fitz
from docx import Document


class ResumeParser:
    """Extracts text from PDF and DOCX resumes."""

    @staticmethod
    def extract_text(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return ResumeParser._extract_pdf(file_path)

        if extension == ".docx":
            return ResumeParser._extract_docx(file_path)

        raise ValueError("Unsupported file type.")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        document = fitz.open(file_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)