import os
import json
import logging
from fastapi import FastAPI, Request, Response
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDS_JSON = json.loads(os.getenv("GOOGLE_CREDS_JSON"))

RAILWAY_URL = os.getenv("RAILWAY_STATIC_URL") or os.getenv("PUBLIC_URL")
if not RAILWAY_URL:
    raise RuntimeError("Не задан публичный URL проекта")

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{RAILWAY_URL}{WEBHOOK_PATH}"

app = FastAPI()
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Пример простого хендлера
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот.")

application.add_handler(CommandHandler("start", start))

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return Response(status_code=200)

async def on_startup():
    logging.info(f"Setting webhook to {WEBHOOK_URL}")
    await bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(on_startup())
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
