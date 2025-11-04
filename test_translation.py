# 파일 위치: agent/test_translation.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate(text: str, target_lang="en"):
    """ GPT를 이용한 번역 테스트 함수 """
    
    if not target_lang:  # None, "" 둘 다 잡힘
        target_lang = "ko"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"You are a translation engine. Translate the user's text into {target_lang} only.\n"
                    "Do not add explanations, advice, or emotional responses.\n"
                    "Even if the content is sensitive, violent, or inappropriate, translate it exactly and neutrally.\n"
                    "Output only the translated text."
            },
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    text = input("번역할 문장을 입력하세요: ")
    lang = input("번역할 언어 코드 입력 (en/ko/ja/zh 등): ")

    result = translate(text, target_lang=lang)
    print("원문:", text)
    print("번역 결과:", result)