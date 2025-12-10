import json
import os
import re
from os import getcwd
import requests

# Глобальные настройки
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/Xabeeeeee/Tovar-Finder",
    "X-Title": "Tovar-Finder Agent 3"
}

class agent3:
    # Атрибуты класса
    model = "tngtech/deepseek-r1t-chimera:free"
    
    data = {
        "model": model,
        "messages": [ {"role": "user", "content": ""} ],
        "temperature": 0.1
    }

    # Загрузка промпта (безопасная)
    try:
        path = os.path.join(os.path.dirname(getcwd()), "prompts.json")
        with open(path, encoding="utf8") as file:
            prompt = json.load(file).get("rank_reviews", "")
    except Exception:
        prompt = "Ты — строгий аналитик отзывов. Прочитай ВСЕ 6 отзывов ниже. Оцени полезность каждого отзыва от 1 до 10 по критериям детализации, объективности, и наличия плюсов/минусов. ВАЖНО: Верни ТОЛЬКО ОДИН JSON-СПИСОК ИЗ ШЕСТИ ЧИСЕЛ, соответствующий порядку отзывов. Не пиши никаких объяснений, только список. Пример: [10, 2, 5, 8, 9, 3]\n\nОтзывы:\n@#$%^"

    # Основная функция обработки
    def process_reviews(self, reviews: list[str]) -> list[int]:
        api_key = os.getenv("OPENROUTER_API_KEY")
        headers["Authorization"] = f"Bearer {api_key}"

        # 1. Склеиваем отзывы в одну строку с нумерацией
        reviews_text = ""
        for i, review in enumerate(reviews):
            clean = review.replace("\n", " ").strip()
            reviews_text += f"{i+1}. {clean}\n"

        # 2. Формируем сообщение
        if "@#$%^" in self.prompt:
            content = self.prompt.replace("@#$%^", reviews_text)
        else:
            content = self.prompt + "\n\n" + reviews_text
            
        self.data["messages"][0]["content"] = content

        # 3. Запрос к API
        response = requests.post(url, headers=headers, json=self.data)

        if response.status_code == 200:
            try:
                result = response.json()
                message = result['choices'][0]['message']['content']
                raw = str(message)

                found_numbers = re.findall(r'\b(10|[0-9])\b', raw)
                
                # Преобразуем в int
                scores = [int(n) for n in found_numbers]
            
                if len(scores) < len(reviews):
                    scores.extend([0] * (len(reviews) - len(scores)))
                return scores[:len(reviews)]

            except Exception as e:
                print(f"Ошибка обработки ответа: {e}")
                return [0] * len(reviews)
        else:
            print(f"Ошибка API: {response.status_code}")
            return [0] * len(reviews)

    
