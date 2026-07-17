import os
import asyncio
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


async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
