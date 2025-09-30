# retrieval_test.py
import argparse
from modules.retriever import query_collection

def main():
    parser = argparse.ArgumentParser(description="Test Retrieval from ChromaDB")
    parser.add_argument(
        "--collection", 
        type=str, 
        required=True, 
        help="Tên collection đã lưu embeddings"
    )
    parser.add_argument(
        "--query", 
        type=str, 
        required=True, 
        help="Câu hỏi từ người dùng"
    )
    parser.add_argument(
        "--top_k", 
        type=int, 
        default=5, 
        help="Số chunks muốn lấy (default=5)"
    )
    args = parser.parse_args()

    context = query_collection(args.collection, args.query, top_k=args.top_k)

    if context:
        print("\n🔎 Context tìm thấy:\n")
        print(context)
    else:
        print("\n⚠️ Không tìm thấy thông tin phù hợp.")

if __name__ == "__main__":
    main()
