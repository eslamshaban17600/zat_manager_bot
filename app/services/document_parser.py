import os
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from app.core.logging_config import logger

async def extract_text_from_file(file_path: str, file_extension: str) -> str:
    """
    استخراج النصوص من ملفات PDF أو Word بدقة.
    """
    extracted_text = ""
    try:
        if file_extension.lower() == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        elif file_extension.lower() in [".docx", ".doc"]:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    extracted_text += paragraph.text + "\n"
        else:
            raise ValueError("نوع الملف غير مدعوم. يرفع ملف PDF أو Word فقط.")
        
        return extracted_text.strip()
    except Exception as e:
        logger.error(f"خطأ أثناء استخراج النص من الملف {file_path}: {e}")
        return ""