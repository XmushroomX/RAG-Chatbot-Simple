from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
import os

def load_document(file_path: str):
    """Load file PDF/DOCX/TXT"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Không hỗ trợ định dạng file: {ext}")
    return loader.load()
