# generation_test.py
import argparse
from modules.generator import generate_answer

def main():
    parser = argparse.ArgumentParser(description="Test Phase 4 - Generation with Groq")
    parser.add_argument("--collection", type=str, required=True, help="Tên collection")
    parser.add_argument("--query", type=str, required=True, help="Câu hỏi từ user")
    parser.add_argument("--model", type=str, default="llama-3.1-8b-instant", help="Tên model Groq")
    args = parser.parse_args()

    answer = generate_answer(args.collection, args.query, top_k=5, model=args.model)

    print("\n🤖 Câu trả lời:\n")
    print(answer)

if __name__ == "__main__":
    main()
