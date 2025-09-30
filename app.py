# app.py
import os
import streamlit as st
from modules import embed_store, generator

# ==========================
# INIT
# ==========================
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("📄 RAG Chatbot powered by Groq + ChromaDB")

# Khởi tạo lớp lưu trữ embedding
store = embed_store.EmbedStore(collection_name="rag_collection")

# ==========================
# SIDEBAR: UPLOAD FILE
# ==========================
st.sidebar.header("📂 Upload tài liệu")
uploaded_files = st.sidebar.file_uploader(
    "Chọn file PDF, DOCX, hoặc TXT",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        temp_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Thêm vào vector DB (chung collection)
        try:
            store.add_document(temp_path)
            st.sidebar.success(f"✅ Đã xử lý: {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"❌ Lỗi xử lý {uploaded_file.name}: {e}")

# ==========================
# MAIN CHAT INTERFACE
# ==========================
st.subheader("💬 Chat với tài liệu của bạn")

# Khởi tạo session lưu lịch sử hội thoại
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Input câu hỏi
user_query = st.text_input("Nhập câu hỏi:")

if st.button("Hỏi") and user_query.strip():
    # ==========================
    # RETRIEVAL CONTEXT
    # ==========================
    context_text = ""
    try:
        context_docs = store.similarity_search(user_query, k=5)
        if context_docs:
            context_text = "\n\n".join([doc['text'] for doc in context_docs])
    except Exception as e:
        st.warning(f"Lỗi truy xuất context: {e}")

    # ==========================
    # GENERATE ANSWER (không streaming)
    # ==========================
    try:
        # Gom toàn bộ output từ generate_answer_stream
        answer_chunks = generator.generate_answer_stream(user_query, context_text)
        answer_text = "".join([chunk for chunk in answer_chunks])

        st.session_state["chat_history"].append(("🧑", user_query))
        st.session_state["chat_history"].append(("🤖", answer_text))
    except Exception as e:
        st.warning(f"⚠️ Lỗi khi gọi LLM: {e}")

# ==========================
# DISPLAY CHAT HISTORY
# ==========================
for speaker, msg in st.session_state["chat_history"]:
    st.markdown(f"**{speaker}:** {msg}")


