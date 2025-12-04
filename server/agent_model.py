import json
import os
from os import getcwd

import requests

path = ""
url = "https://openrouter.ai/api/v1/chat/completions"

with open(os.path.dirname(getcwd()) + "\\prompts.json", encoding="utf8") as file:
    # Convert JSON file content to a Python dictionary
    prompts = json.load(file)

def process_input(inp: str) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "tngtech/deepseek-r1t-chimera:free",  # Можно выбрать другую модель
        "messages": [
            {"role": "user",
             "content": prompts["process_input"].replace("@#$%^", inp)}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        # Извлекаем ответ модели
        message = result['choices'][0]['message']['content']
        raw = str(message)
        js = json.loads(message[raw.find("{"): raw.find("}") + 1])
        print(js)
        return js
        # Дополнительная информация
        # print("\n--- Метаданные ---")
        # print(f"Модель: {result['model']}")
        # print(f"Использовано токенов: {result['usage']['total_tokens']}")
    else:
        return dict()
    # print(f"Ошибка: {response.status_code}")
    # print(response.text)

