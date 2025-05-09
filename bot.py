import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from sheets_connector import write_to_sheet
from kcal_parser import parse_kcal

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDS_JSON = json.loads(os.getenv("GOOGLE_CREDS_JSON"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Helpik. Отправь приём пищи, и я его запишу.")

async def handle_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    kcal_data = parse_kcal(text)
    row = {
        "Дата": update.message.date.strftime("%Y-%m-%d"),
        "Время": update.message.date.strftime("%H:%M"),
        "Прием пищи": text,
        **kcal_data
    }

    success = write_to_sheet(row, SPREADSHEET_ID, GOOGLE_CREDS_JSON)
    if success:
        await update.message.reply_text("Записал приём пищи в таблицу ✅")
    else:
        await update.message.reply_text("Ошибка при записи в таблицу ❌")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_food))
    app.run_polling()
