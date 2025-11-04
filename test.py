# 파일 위치: agent/test_translation.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ .env 파일 불러오기 (agent 폴더 기준)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate(text: str, target_lang="en"):
    """ GPT를 이용한 번역 테스트 함수 """
    response = client.chat.completions.create(
        model="gpt-4o",  # → 원하는 경우 gpt-4o-mini로 변경 가능
        messages=[
            {
                "role": "system",
                "content": f"You are a translator that translates text into {target_lang} naturally and accurately."
            },
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # ✅ 여기서 바로 번역 테스트 가능
    original_text = "Long time no see! Hi, how have you been? The weather is really nice today!"
    result = translate(original_text, target_lang="en")
    print("📝 원문:")
    print(original_text)
    print("✅ 번역 결과:")
    print(result)
