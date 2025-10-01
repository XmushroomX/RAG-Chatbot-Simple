# 📚 RAG Chatbot với Groq API + Streamlit + ChromaDB

Dự án này xây dựng một chatbot dạng **RAG (Retrieval-Augmented Generation)** sử dụng:
- **Streamlit** để tạo giao diện web
- **ChromaDB** để lưu trữ và truy xuất vector
- **Groq API** làm LLM backend
- **LangChain** để kết nối các thành phần

---

## 🚀 1. Cài đặt môi trường

### 1.1. Clone repo
```bash
git clone https://github.com/XmushroomX/RAG-Chatbot-Simple.git
cd rag-chatbot
```

### 1.2. Tạo virtual environment (khuyến nghị dùng `conda`)
```bash
conda create -n rag-chatbot python=3.11 -y
conda activate rag-chatbot
```

Hoặc dùng `venv`:
```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / MacOS
.venv\Scripts\activate      # Windows
```

### 1.3. Cài dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 2. Cấu hình API Key

Bạn cần có **Groq API key**.  
Đặt biến môi trường sau trong hệ thống:

**Linux / MacOS**
```bash
export GROQ_API_KEY="your_api_key_here"
```

**Windows (PowerShell)**
```powershell
setx GROQ_API_KEY "your_api_key_here"
```

Hoặc tạo file `.env` trong thư mục gốc của dự án:
```
GROQ_API_KEY=your_api_key_here
```

---

## 🖥️ 3. Chạy ứng dụng

Sau khi cài đặt xong, chạy Streamlit:
```bash
streamlit run app.py
```

Ứng dụng sẽ chạy tại:
👉 http://localhost:8501

---



---

## ⚡ 4. Demo workflow

1. Người dùng tải tài liệu (PDF, DOCX, TXT).
2. Tài liệu được nhúng vector bằng **sentence-transformers** và lưu vào **ChromaDB**.
3. Khi đặt câu hỏi, hệ thống truy xuất đoạn văn bản liên quan từ ChromaDB.
4. Groq API sinh câu trả lời dựa trên ngữ cảnh + câu hỏi.

---

## 📌 5. Ghi chú
- Hỗ trợ nhiều loại tài liệu: `.pdf`, `.docx`, `.txt`.
- Mặc định model Groq: `openai/gpt-oss-20b`.

---
