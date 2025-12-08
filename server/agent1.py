import json
import os
from os import getcwd

import requests

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "",
    "Content-Type": "application/json",
}

class agent1:
    model = "tngtech/deepseek-r1t-chimera:free"

    data = {
        "model": model,
        "messages": [ {"role": "user", "content": ""} ]
    }

    with open(os.path.dirname(getcwd()) + "\\prompts.json", encoding="utf8") as file:
        # Convert JSON file content to a Python dictionary
        prompt = json.load(file)["process_input"]


    # Агент 1: преобразование описания
    def process_input(self, inp: str):
        api_key = os.getenv("OPENROUTER_API_KEY")
        headers["Authorization"] = f"Bearer {api_key}"
        self.data["messages"][0]["content"] = self.prompt.replace("@#$%^", inp)

        response = requests.post(url, headers=headers, json=self.data)

        if response.status_code == 200:
            result = response.json()
            # Извлекаем ответ модели
            message = result['choices'][0]['message']['content']
            raw = str(message)
            js = message[raw.find("{"): raw.find("}") + 1]
            return js
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return ""
