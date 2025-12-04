import json
import os
from os import getcwd

import requests

path = ""
url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("OPENROUTER_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
model = "tngtech/deepseek-r1t-chimera:free"
data = {
        "model": model,
        "messages": [
            {"role": "user",
             "content": ""}
        ]
    }

with open(os.path.dirname(getcwd()) + "\\prompts.json", encoding="utf8") as file:
    # Convert JSON file content to a Python dictionary
    prompts = json.load(file)


def process_input(inp: str):
    data["messages"][0]["content"] = prompts["process_input"].replace("@#$%^", inp)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        # Извлекаем ответ модели
        message = result['choices'][0]['message']['content']
        raw = str(message)
        js = message[raw.find("{"): raw.find("}") + 1]
        print(js)
        return js
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        return ""


def process_query(query: str):
    try:
        data["messages"][0]["content"] = prompts["find_offers"].replace("{}", query)
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            # Извлекаем ответ модели
            message = result['choices'][0]['message']['content']
            raw = str(message)
            js = message[raw.find("["): raw.find("]") + 1]
            print(js)
            return js
        else:
            return ""
    except KeyError:
        return ""