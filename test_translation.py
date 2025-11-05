# 파일 위치: agent/test_translation.py

import os
from dotenv import load_dotenv
from openai import OpenAI
import deepl  # ✅ DeepL import 필수

# ===== ① OpenAI 설정 (.env 사용) =====
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== ② DeepL API Key 하드코딩 (여기에 직접 입력) =====
DEEPL_API_KEY = "92324edc-b0d5-49d6-8d81-02ce8e681d92:fx"  # 🔹 여기를 본인 키로 수정
deepl_translator = deepl.Translator(DEEPL_API_KEY) if DEEPL_API_KEY else None


# ✅ 입력 언어 자동 감지 (GPT 사용)
def detect_language(text: str) -> str:
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


# ✅ GPT 번역 함수
def translate_gpt(text: str, target_lang="en"):
    source_lang = detect_language(text)

    if not target_lang:
        target_lang = "ko"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a translation engine. Translate the user's text into {target_lang} only.\n"
                    "Do not add explanations, advice, or emotions.\n"
                    "Output only the translated text."
                )
            },
            {"role": "user", "content": text}
        ]
    )
    translated_text = response.choices[0].message.content
    return translated_text, source_lang, target_lang


# ✅ DeepL 번역 함수 (하드코딩으로 실행)
def translate_deepl(text: str, target_lang="KO"):
    if not deepl_translator:
        return "❌ DeepL API Key가 설정되지 않았습니다."
    result = deepl_translator.translate_text(text, target_lang=target_lang)
    return result.text, target_lang


# ✅ 메인 실행 (GPT vs DeepL 비교)
if __name__ == "__main__":
    text = """
Over the past few years, the global economy has entered a period of rapid transformation driven by artificial intelligence, digital platforms, and geopolitical uncertainty. Countries that once depended on manufacturing and cheap labor are now competing to lead in AI, renewable energy, and advanced data technologies. South Korea, long known for its semiconductor and electronics industries, is at a turning point. Experts say that relying only on hardware production is no longer enough in an era where creativity, data, and innovation hold greater value.

A recent report from the World Economic Forum suggests that nations that invest in digital infrastructure, education, and responsible AI policies will experience more resilient growth. However, this transition comes with serious challenges. Automation powered by AI is expected to replace millions of jobs, particularly in transportation, finance, and administration. Yet history shows that technological revolutions not only destroy jobs but also create new ones. The report notes, “The real threat is not that machines will replace humans, but that societies may fail to adapt and redefine the meaning of work.”

Interestingly, many young people view this change with optimism. They believe that if repetitive tasks are handled by machines, humans will finally have more time for creativity, research, and meaningful innovation. But critics argue this future will only be possible if governments and companies take responsibility for re-education, social safety nets, and fair opportunities.

In the end, the real question is not how powerful technology will become, but how wisely humanity will choose to use it.
"""

    # 🔹 GPT 번역
    gpt_result, detected_lang, target_lang = translate_gpt(text, "ko")

    # 🔹 DeepL 번역
    deepl_result, deepl_target = translate_deepl(text, "KO")

    print("\n==== ✅ GPT-4 번역 ====")
    print(f"- 감지된 언어: {detected_lang}")
    print(f"- 번역 결과:\n{gpt_result}")

    print("\n==== ✅ DeepL 번역 ====")
    print(f"- 번역 결과:\n{deepl_result}")
