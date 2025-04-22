import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
# Используем Meta: Llama 4 Maverick (free) в OpenRouter
MODEL_ID = "meta-llama/llama-4-maverick:free"

# Системная инструкция для избегания галлюцинаций и ТОЧНО русскоязычные ответы, у других моделей даже с этим были проблемы
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Ты — разговариваешь только на русском языке если пользователь не попросит иного. "
        "Отвечай по фактам, приводи точные данные. "
        "Не выдумывай информацию. Если не знаешь — скажи \"Не знаю\"."
    )
}

# Функция отправки запроса к OpenRouter

def ask_openrouter(user_input, history=None):
    if history is None:
        history = []

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Собираем сообщения: системная инструкция, история, новый пользовательский запрос
    messages = [SYSTEM_PROMPT] + history + [{"role": "user", "content": user_input}]

    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": 0.0,
        "top_p": 1.0,
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        # Читаем ответ модели
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"[Ошибка при обращении к API: {e}]"
    except (KeyError, IndexError, ValueError):
        return "[Ошибка: неожиданный формат ответа от API]"


