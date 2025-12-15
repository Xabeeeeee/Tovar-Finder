import json
import os
from os import getcwd

import requests

url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("OPENROUTER_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/Xabeeeeee/Tovar-Finder",
    "X-Title": "Tovar-Finder Agent 2"
}

class agent2:
    model = "tngtech/deepseek-r1t-chimera:free"
    data = {
        "model": model,
        "messages": [{"role": "user", "content": ""}],
        "temperature": 0.1
    }

    with open(os.path.dirname(getcwd()) + "\\prompts.json", encoding="utf8") as file:
        prompt = json.load(file)["find_offers"]

    # Агент 2: генерация моделей
    def process_query(self, query: str):
        self.data["messages"][0]["content"] = self.prompt.replace("{}", query)
        response = requests.post(url, headers=headers, json=self.data)

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            raw = str(message)
            js = message[raw.find("["): raw.find("]") + 1]
            return js
        else:
            raise ConnectionError
