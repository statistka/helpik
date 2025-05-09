import os
import logging
import json
from aiohttp import web
from telegram import Update
from telegram.ext import Application

from bot import get_application

logging.basicConfig(level=logging.INFO)

# Telegram Application
application: Application = get_application()

# Обработчик входящих webhook-запросов от Telegram
async def handle_webhook(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return web.Response(text="OK")
    except Exception as e:
        logging.exception("❌ Ошибка обработки Webhook: %s", e)
        return web.Response(status=500, text="Internal Server Error")

def main():
    app = web.Application()
    app.router.add_post("/webhook", handle_webhook)

    port = int(os.getenv("PORT", 8080))
    logging.info(f"🚀 Helpik запущен на порту {port}")
    web.run_app(app, port=port)

if __name__ == "__main__":
    main()
