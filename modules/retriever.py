# retriever.py
from modules.embed_store import EmbedStore

# Tạo instance EmbedStore dùng chung
store = EmbedStore()


def retrieve_context(query: str, k: int = 5):
    """
    Truy xuất top-k chunks liên quan đến query từ EmbedStore.
    Trả về list các dict: {text, source, chunk_id, score}
    """
    try:
        contexts = store.similarity_search(query, k)
        return contexts
    except Exception as e:
        print(f"Lỗi truy xuất context: {e}")
        return []


def build_context_string(query: str, k: int = 5):
    """
    Xây dựng context string từ các chunk truy xuất được
    để đưa vào prompt LLM.
    """
    contexts = retrieve_context(query, k)
    if not contexts:
        return ""
    
    context_texts = [
        f"[{c['source']} - chunk {c['chunk_id']}] {c['text']}"
        for c in contexts
    ]
    return "\n\n".join(context_texts)
