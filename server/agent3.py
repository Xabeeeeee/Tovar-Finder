import json
import requests
import re
import os
from typing import List, Dict, Any

class Agent3:
    def __init__(self, api_key: str, model: str, threshold: int = 7):
        """
        Инициализация Агента 3.
        """
        self.api_key = api_key
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = model
        self.threshold = threshold
        
        # Базовый промпт из ТЗ
        self.base_system_prompt = (
            "Ты - помощник для покупателя. Проанализируй представленный ниже отзыв на {product_name} "
            "и оцени его полезность для потенциального покупателя по следующим критериям:\n\n"
            "1. **Информативность и детализация:**\n"
            " * Содержит ли отзыв конкретные факты о характеристиках?\n"
            " * Описан ли личный опыт использования?\n\n"
            "2. **Анализ достоинств и недостатков:**\n"
            " * Упомянуты ли не только плюсы, но и конструктивные минусы?\n"
            " * Являются ли недостатки критичными?\n\n"
            "3. **Обоснованность и объективность:**\n"
            " * Подкреплены ли оценки аргументами?\n"
            " * Чувствуется ли эмоциональный окрас без фактов?\n\n"
            "4. **Уникальность и ответы на скрытые вопросы:**\n"
            " * Раскрывает ли отзыв скрытые нюансы?\n\n"
            "**Задание:**\n"
            "Численно оцени полезность отзыва по шкале от 1 до 10.\n\n"
            "**Формат ответа**: одно число от 1 до 10 - степень полезности отзыва, никакие пояснения приводить не нужно."
        )

    def _get_score_from_api(self, review_text: str, product_name: str) -> int:
        """Отправляет запрос в LLM через OpenRouter и получает оценку."""
        
        system_prompt = self.base_system_prompt.format(product_name=product_name)
        user_content = f"**Текст отзыва для анализа:**\n{review_text}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "Tovar-Finder Agent 3"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1, 
            "max_tokens": 10
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            
            content = result['choices'][0]['message']['content'].strip()
            
            match = re.search(r'\b(10|[1-9])\b', content)
            if match:
                return int(match.group(0))
            else:
                print(f"[Agent 3] Warning: Could not parse number from response: {content}")
                return 0 
                
        except Exception as e:
            print(f"[Agent 3] Error calling OpenRouter: {e}")
            return 0

    def process_data(self, input_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основной метод. Принимает JSON с продуктом и комментариями,
        фильтрует их и возвращает обновленный JSON.
        """
        product_name = input_json.get("product_name", "товар")
        raw_reviews = input_json.get("raw_reviews", [])
        
        processed_reviews = []
        
        print(f"--- Agent 3: Анализ отзывов для '{product_name}' ---")
        
        for review in raw_reviews:
            if len(review) < 10:
                continue
                
            score = self._get_score_from_api(review, product_name)
            
            print(f"Review score: {score} | Preview: {review[:30]}...")
            
            if score >= self.threshold:
                processed_reviews.append({
                    "text": review,
                    "usefulness_score": score
                })

        processed_reviews.sort(key=lambda x: x['usefulness_score'], reverse=True)

        output_json = input_json.copy()
        output_json["selected_reviews"] = processed_reviews
        if "raw_reviews" in output_json:
            del output_json["raw_reviews"]
            
        return output_json


if __name__ == "__main__":
    
    API_KEY = "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"
    
    # 1. Имя входного файла
    input_filename = "input.json"
    
    # 2. Попытка загрузить данные из файла
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            # json.load() считывает данные из файла в переменную test_input
            test_input = json.load(f)
        
        print(f"✅ Данные успешно загружены из {input_filename}")
        
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл {input_filename} не найден в текущей директории. Создайте его и запустите снова.")
        exit()
    except json.JSONDecodeError:
        print(f"❌ Ошибка: Файл {input_filename} содержит невалидный JSON. Проверьте его структуру.")
        exit()
    except Exception as e:
        print(f"❌ Неизвестная ошибка при чтении файла: {e}")
        exit()


    # Инициализация агента
    agent = Agent3(api_key=API_KEY, model="tngtech/deepseek-r1t-chimera:free") 
    
    # 3. Запуск обработки
    result = agent.process_data(test_input)
    
    # 4. Имя файла для сохранения
    output_filename = "output.json"

    # 5. Вывод результата в консоль и запись в файл
    print("\n--- RESULT JSON (Консольный вывод) ---")
    output_content = json.dumps(result, ensure_ascii=False, indent=4)
    print(output_content)

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        print(f"\n✅ Результат успешно сохранен в файл: {output_filename}")
        
    except Exception as e:
        print(f"\n❌ Ошибка при записи файла {output_filename}: {e}")
