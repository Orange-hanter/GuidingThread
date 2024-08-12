import os

from openai import OpenAI
from dotenv import load_dotenv, dotenv_values

"""
    Для работы нужен токен, создать переменную окружения OPENAI_API_KEY
"""
load_dotenv()
client = OpenAI(api_key=os.getenv("MY_KEY"))


def request_extraction_d(prompt):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": """Твоя задача конвертировать текст в последовательный список json структур. Текст из себя представляет инструкцию, последовательность действий, или набор условий если-то. Последовательный список json структур - это шаблонная структура следующего вида { "id": 0-9999, "subject": text "task": text } Ты должен ждать текст и конвертировать его в указанную выше структуру"""},
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


def request_extraction(prompt):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": """Твоя задача конвертировать текст в последовательный список json структур. Текст из себя представляет инструкцию, последовательность действий, или набор условий если-то. Последовательный список json структур - это шаблонная структура следующего вида { "id": 0-9999, "subject": text "task": text } Ты должен ждать текст и конвертировать его в указанную выше структуру"""},
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
    )
    answer = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer = chunk.choices[0].delta.content
    return answer
