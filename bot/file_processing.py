import pdfplumber
from docx import Document

class FileProcessor:
    @staticmethod
    def process_txt(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    @staticmethod
    def process_docx(file_path):
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    @staticmethod
    def process_pdf(file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text