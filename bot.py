import os
import json
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from sheets_connector import (
    write_meal,
    write_hydration,
    write_vitamins,
    write_workout
)
from kcal_parser import parse_kcal

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDS_JSON = json.loads(os.getenv("GOOGLE_CREDS_JSON"))

def extract_date_and_text(message: str):
    message = message.strip()
    if len(message) >= 11 and message[2] == "." and message[5] == "." and message[10] == ":":
        try:
            date = datetime.strptime(message[:10], "%d.%m.%Y").strftime("%Y-%m-%d")
            return date, message[11:].strip()
        except:
            pass
    return datetime.now().strftime("%Y-%m-%d"), message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я Helpik — твой трекер питания, воды, витаминов и активности.\n\n"
        "📌 Я понимаю такие форматы:\n"
        "🍽 `завтрак: овсянка 200г, мёд 20г`\n"
        "💧 `гидро: вода 1300 мл, кофе 600 мл`\n"
        "💊 `витамины: омега-3, К2`\n"
        "🏃‍♀️ `нагрузка: бег интенсивный 30 мин, йога 60 мин`\n\n"
        "📆 Можно указывать дату вручную:\n"
        "`08.05.2025: ужин: гречка, яйца 2шт`"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    date, message = extract_date_and_text(text)

    if message.startswith(("завтрак:", "обед:", "ужин:", "полдник:", "перекус:")):
        meal_type, description = message.split(":", 1)
        kcal_data = parse_kcal(description)
        write_meal(GOOGLE_CREDS_JSON, SPREADSHEET_ID, date, meal_type.strip(), description.strip(), kcal_data)
        await update.message.reply_text("🍽 Питание записано!")

    elif message.startswith("гидро:"):
        water_ml = 0
        caffeine_ml = 0

        for part in message.split(","):
            part = part.strip()
            if part.startswith("вода"):
                try:
                    water_ml = int(part.split("вода")[1].split("мл")[0].strip())
                except: pass
            elif part.startswith("кофе"):
                try:
                    caffeine_ml = int(part.split("кофе")[1].split("мл")[0].strip())
                except: pass

        write_hydration(GOOGLE_CREDS_JSON, SPREADSHEET_ID, date, water_ml, caffeine_ml)
        await update.message.reply_text("💧 Гидратация записана!")

    elif message.startswith("витамины:"):
        description = message.replace("витамины:", "").strip()
        write_vitamins(GOOGLE_CREDS_JSON, SPREADSHEET_ID, date, description)
        await update.message.reply_text("💊 Витамины записаны!")

    elif message.startswith("нагрузка:"):
        text_body = message.replace("нагрузка:", "").strip()
        parts = text_body.split(",")
        workout_data = {}
        for part in parts:
            part = part.strip()
            for activity in ["разминка", "бег интенсивный", "бег лёгкий", "силовая", "йога", "велосипед", "плавание", "хайкинг", "ходьба"]:
                if activity in part:
                    try:
                        minutes = int(part.split(activity)[1].split("мин")[0].strip())
                        workout_data[activity] = minutes
                    except:
                        workout_data[activity] = 0
        write_workout(GOOGLE_CREDS_JSON, SPREADSHEET_ID, date, workout_data)
        await update.message.reply_text("🏃‍♀️ Нагрузка записана!")

    else:
        await update.message.reply_text(
            "❓ Не могу распознать сообщение. Форматы:\n"
            "🍽 завтрак: ...\n"
            "💧 гидро: ...\n"
            "💊 витамины: ...\n"
            "🏃 нагрузка: ...\n"
            "📅 Можно указать дату: `08.05.2025: завтрак: ...`"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
