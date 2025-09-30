import os

# Đường dẫn lưu ChromaDB
CHROMA_PATH = os.path.join(os.getcwd(), "chroma_store")

# Model embedding OSS
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Thư mục lưu file upload
UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
