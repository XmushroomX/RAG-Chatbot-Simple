# generator.py
from groq import Groq

client = Groq()
MODEL_NAME = "openai/gpt-oss-20b"

def generate_answer_stream(query: str, context: str = ""):
    """
    Streaming từng phần câu trả lời từ LLM.
    """
    prompt = f"""
Bạn là trợ lý AI. Trả lời câu hỏi dựa trên ngữ cảnh nếu có. Nếu không biết, hãy trả lời thành thật rằng bạn không biết.
Ngữ cảnh:
{context}

Câu hỏi: {query}
Trả lời:
    """

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=8192,
        top_p=1,
        stream=True,
        stop=None
    )

    # Chỉ yield khi có nội dung mới
    seen_text = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            yield content
