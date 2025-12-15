import json
import os
import re
from os import getcwd

import requests

url = "https://openrouter.ai/api/v1/chat/completions"
api_key = os.getenv("OPENROUTER_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/Xabeeeeee/Tovar-Finder",
    "X-Title": "Tovar-Finder Agent 3"
}

class agent3:
    model = "tngtech/deepseek-r1t-chimera:free"
    data = {
        "model": model,
        "messages": [ {"role": "user", "content": ""} ],
        "temperature": 0.1
    }

    with open(os.path.dirname(getcwd()) + "\\prompts.json", encoding="utf8") as file:
        prompt = json.load(file)["rank_reviews"]

    # Агент 3: оценка полезности отзыва
    def process_reviews(self, reviews: list[dict]) -> list[int]:
        reviews_text = "\n\n"
        for i, review in enumerate(reviews):
            clean = review["desc"].replace("\n", "\t").strip()
            reviews_text += f"{i+1}. {clean}\n"
            
        self.data["messages"][0]["content"] = self.prompt + reviews_text
        response = requests.post(url, headers=headers, json=self.data)

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            raw = str(message)
            found_numbers = re.findall(r'\b(10|[0-9])\b', raw)
            scores = [int(n) for n in found_numbers]
            if len(scores) < len(reviews):
                scores.extend([0] * (len(reviews) - len(scores)))
            return scores[:len(reviews)]
        else:
            raise ConnectionError
