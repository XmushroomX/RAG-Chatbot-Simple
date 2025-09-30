import os
from config.settings import UPLOAD_DIR

def save_uploaded_file(uploaded_file):
    """Lưu file upload vào thư mục uploads"""
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
