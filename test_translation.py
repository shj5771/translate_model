# 파일 위치: agent/test_translation.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_language(text: str) -> str:
    """입력된 문장이 어떤 언어인지 감지 (ko, en, ja, zh 등)"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a language detector. "
                           "Respond ONLY with the ISO 639-1 language code (ex: ko, en, ja, zh, fr, de)."
            },
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip().lower()

def translate(text: str, target_lang="en"):
    """ GPT를 이용한 번역 테스트 함수 """
    source_lang = detect_language(text)  # ① 입력 언어 감지

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
    translated_text = response.choices[0].message.content
    return translated_text, source_lang, target_lang

if __name__ == "__main__":
    text = input("번역할 문장을 입력하세요: ")
    lang = input("번역할 언어 코드 입력 (비우면 자동 한국어): ")

    result, detected, target = translate(text, lang)
    print(f"\n 감지된 입력 언어: {detected}")
    print(f" 번역 목표 언어: {target}")
    print(f"원문:", text)
    print(f"번역 결과: {result}")