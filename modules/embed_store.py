# embed_store.py
import os
import uuid
import chromadb
import torch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbedStore:
    def __init__(self, collection_name: str = "rag_collection"):
        # ======================
        # DEVICE SELECTION
        # ======================
        if torch.cuda.is_available():
            device = "cuda"
            print("✅ Sử dụng GPU (CUDA)")
        elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            device = "mps"
            print("✅ Sử dụng GPU (MPS - Apple Silicon)")
        else:
            device = "cpu"
            print("⚠️ Không tìm thấy GPU, fallback về CPU")

        # ======================
        # COLLECTION + EMBEDDING
        # ======================
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.get_or_create_collection(self.collection_name)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": device}
        )
        self.embedding_dim = 384  # all-MiniLM-L6-v2 có embedding dimension = 384

    # ======================
    # COLLECTION MANAGEMENT
    # ======================
    def get_or_create_collection(self, collection_name: str):
        try:
            collection = self.client.get_collection(collection_name)
        except Exception:
            collection = self.client.create_collection(collection_name)
        return collection

    # ======================
    # FILE LOADERS
    # ======================
    @staticmethod
    def load_file(file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        return loader.load()

    # ======================
    # CHUNKING
    # ======================
    @staticmethod
    def chunk_documents(documents, chunk_size: int = 500, chunk_overlap: int = 50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        return splitter.split_documents(documents)

    # ======================
    # FILE EMBEDDING
    # ======================
    def file_already_embedded(self, file_name: str) -> bool:
        try:
            results = self.collection.query(
                query_embeddings=[[0.0] * self.embedding_dim],
                n_results=1,
                include=["metadatas"]
            )
            for meta in results.get("metadatas", [[]])[0]:
                if isinstance(meta, dict) and meta.get("source") == file_name:
                    return True
            return False
        except Exception:
            return False

    def process_files(self, uploaded_files):
        """
        Load, chunk, embed and store documents in Chroma.
        """
        for file in uploaded_files:
            if hasattr(file, "name"):
                file_name = file.name
                file_path = os.path.join("uploads", file_name)
                os.makedirs("uploads", exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(file.read())
            else:
                file_path = file
                file_name = os.path.basename(file_path)

            # Skip if already embedded
            if self.file_already_embedded(file_name):
                print(f"⚠️ File {file_name} đã được embed trước đó, bỏ qua.")
                continue

            # Load + chunk
            docs = self.load_file(file_path)
            chunks = self.chunk_documents(docs)

            if not chunks:
                print(f"⚠️ Không có nội dung để embed trong file {file_name}.")
                continue

            texts = [chunk.page_content for chunk in chunks]
            metadatas = [{"source": file_name, "chunk_id": str(i)} for i in range(len(chunks))]
            ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
            vectors = self.embeddings.embed_documents(texts)

            self.collection.add(
                ids=ids,
                embeddings=vectors,
                documents=texts,
                metadatas=metadatas
            )
            print(f"✅ Processed {file_name} với {len(chunks)} chunks.")

    def add_document(self, file: str):
        self.process_files([file])

    # ======================
    # SIMILARITY SEARCH
    # ======================
    def similarity_search(self, query: str, k: int = 5):
        try:
            query_vector = self.embeddings.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            contexts = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            ):
                contexts.append({
                    "text": doc,
                    "source": meta.get("source", "unknown") if isinstance(meta, dict) else "unknown",
                    "chunk_id": meta.get("chunk_id", "0") if isinstance(meta, dict) else "0",
                    "score": dist
                })
            return contexts
        except Exception as e:
            print(f"⚠️ Lỗi khi truy xuất context: {e}")
            return []
