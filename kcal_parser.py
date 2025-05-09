# kcal_parser.py

# Простейшая база продуктов: калории, белки, жиры, углеводы на 100 г
PRODUCT_DB = {
    "овсянка": {"kcal": 368, "protein": 12.5, "fat": 6.1, "carbs": 60},
    "банан": {"kcal": 89, "protein": 1.1, "fat": 0.3, "carbs": 23},
    "арахис": {"kcal": 567, "protein": 26, "fat": 49, "carbs": 16},
    "мёд": {"kcal": 304, "protein": 0.3, "fat": 0, "carbs": 82},
    "яйцо": {"kcal": 143, "protein": 13, "fat": 10, "carbs": 1},
    "хлеб": {"kcal": 250, "protein": 8, "fat": 3, "carbs": 50},
    "рис": {"kcal": 130, "protein": 2.7, "fat": 0.3, "carbs": 28},
    "лосось": {"kcal": 208, "protein": 20, "fat": 13, "carbs": 0},
}

import re

def parse_kcal(text):
    total = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
    items = text.lower().split(",")

    for item in items:
        for product in PRODUCT_DB:
            if product in item:
                # Пытаемся вытащить граммы
                match = re.search(r"(\d+)", item)
                grams = int(match.group(1)) if match else 100
                coeff = grams / 100

                total["kcal"] += PRODUCT_DB[product]["kcal"] * coeff
                total["protein"] += PRODUCT_DB[product]["protein"] * coeff
                total["fat"] += PRODUCT_DB[product]["fat"] * coeff
                total["carbs"] += PRODUCT_DB[product]["carbs"] * coeff

    return {
        "Ккал": round(total["kcal"], 1),
        "Белки (г)": round(total["protein"], 1),
        "Жиры (г)": round(total["fat"], 1),
        "Углеводы (г)": round(total["carbs"], 1)
    }
