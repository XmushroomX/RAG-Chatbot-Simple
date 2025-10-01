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

# Tạo thư mục uploads nếu chưa có
os.makedirs("uploads", exist_ok=True)

# Xử lý upload
if uploaded_files:
    for uploaded_file in uploaded_files:
        temp_path = os.path.join("uploads", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Thêm vào vector DB (chung collection)
        try:
            store.add_document(temp_path)
            st.sidebar.success(f"✅ Đã xử lý: {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"❌ Lỗi xử lý {uploaded_file.name}: {e}")

# ==========================
# HIỂN THỊ FILE TRONG THƯ MỤC UPLOAD
# ==========================
st.sidebar.header("📂 Danh sách tài liệu đã upload")
upload_files_list = os.listdir("uploads")
if upload_files_list:
    for f in upload_files_list:
        st.sidebar.markdown(f"- {f}")
else:
    st.sidebar.info("Chưa có file nào được upload.")

# ==========================
# MAIN CHAT INTERFACE
# ==========================
st.subheader("💬 Chat với tài liệu của bạn")

# Khởi tạo session lưu lịch sử hội thoại
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Hiển thị chat history trước (để thanh nhập luôn nằm dưới trang)
for speaker, msg in st.session_state["chat_history"]:
    st.markdown(f"**{speaker}:** {msg}")

# Thanh hỏi đáp ở ĐÁY trang (pinned) — không thay đổi logic xử lý
user_query = st.chat_input("Nhập câu hỏi...")

if user_query and user_query.strip():
    # Lấy context
    context_text = ""
    try:
        context_docs = store.similarity_search(user_query, k=5)
        if context_docs:
            context_text = "\n\n".join([doc['text'] for doc in context_docs])
    except Exception as e:
        st.warning(f"Lỗi truy xuất context: {e}")

    # Sinh câu trả lời
    try:
        answer_text = "".join(generator.generate_answer_stream(user_query, context_text))
        # Lưu lịch sử chat
        st.session_state["chat_history"].append(("🧑", user_query))
        st.session_state["chat_history"].append(("🤖", answer_text))
        # Hiển thị ngay tin nhắn vừa gửi/trả lời (tùy chọn)
        st.markdown(f"**🧑:** {user_query}")
        st.markdown(f"**🤖:** {answer_text}")
    except Exception as e:
        st.error(f"⚠️ Lỗi khi gọi LLM: {e}")
