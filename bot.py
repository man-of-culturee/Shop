import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from dotenv import load_dotenv

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

load_dotenv()
TOKEN = os.getenv("TOKEN")
SHOP_URL = "https://family-home-decor.odoo.com/shop"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(text="Open Shop", web_app=WebAppInfo(url=SHOP_URL))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome to Family Home Decor!", reply_markup=reply_markup
    )


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

    def log_message(self, format, *args):
        pass  # silence default request logging


def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()


def main():
    # Run the fake HTTP server in a background thread so Render detects an open port
    health_thread = Thread(target=run_health_server, daemon=True)
    health_thread.start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
