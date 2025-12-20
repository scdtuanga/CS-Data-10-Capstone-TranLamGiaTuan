from openai import OpenAI

api_key = "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"
client = OpenAI(api_key=api_key)

def analyze_with_ai(summary_text: str) -> str:
    prompt = f"""
    Tôi có dữ liệu phân tích sau:
    {summary_text}

    Hãy viết một báo cáo ngắn bằng tiếng Việt:
    - Nêu rõ vấn đề chính nhìn thấy từ dữ liệu
    - Phân tích chi tiết nguyên nhân
    - Đề xuất một số giải pháp khắc phục
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
