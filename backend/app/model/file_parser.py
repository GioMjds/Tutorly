import os
from typing import IO
from PyPDF2 import PdfReader
import docx

class FileParser:
    """
    Utility class to extract text from PDF, DOCX, and TXT files.
    """
    @staticmethod
    def parse(file: IO, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            return FileParser._parse_pdf(file)
        elif ext == ".docx":
            return FileParser._parse_docx(file)
        elif ext == ".txt":
            return FileParser._parse_txt(file)
        else:
            raise ValueError("Unsupported file type.")

    @staticmethod
    def _parse_pdf(file: IO) -> str:
        try:
            file.seek(0)
            reader = PdfReader(file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text.strip()
        except ImportError:
            raise ImportError("PyPDF2 is required to parse PDF files.")

    @staticmethod
    def _parse_docx(file: IO) -> str:
        try:
            file.seek(0)
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except ImportError:
            raise ImportError("python-docx is required to parse DOCX files.")

    @staticmethod
    def _parse_txt(file: IO) -> str:
        file.seek(0)
        return file.read().decode("utf-8", errors="ignore").strip()
