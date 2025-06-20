from flask import Flask
from threading import Thread
import requests
import time
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

TELEGRAM_BOT_TOKEN = '7413469925:AAGfVC48BAAilkOO_yk-li2v6xg9duG2inU'
TELEGRAM_CHAT_ID = '6065493589'

closing_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42,
                  45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00,
                  46.03, 46.41, 46.22, 45.64, 46.21]

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=payload)

running = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = True
    await update.message.reply_text("Signal service started!")
    while running:
        message = f"Trading Signal:\nPrice: {closing_prices[-1]}\nSignal: BUY (RSI below 30)"
        send_telegram_message(message)
        await asyncio.sleep(180)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = False
    await update.message.reply_text("Signal service stopped!")

async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    await application.run_polling()

keep_alive()
asyncio.run(main())
