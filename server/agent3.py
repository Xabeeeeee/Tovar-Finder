def process_reviews(reviews : list[str]) -> list[int]:
    try:
        data["messages"][0]["content"] = prompts["rank_reviews"]
        for i, review in enumerate(reviews):
            data["messages"][0]["content"] += f"{i}. {review}\n"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            # Извлекаем ответ модели
            message = result['choices'][0]['message']['content']
            raw = str(message)
            print(raw)
            return list(map(int, raw))
        else:
            return ""
    except KeyError:
        return ""
