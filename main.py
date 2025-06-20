from flask import Flask
from threading import Thread
import requests
import time
from telegram.ext import Updater, CommandHandler

app = Flask('')

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

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Signal service started!")
    while True:
        message = "✅ Signal: BUY (Test)"
        send_telegram_message(message)
        time.sleep(180)

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Signal service stopped!")
    exit(0)

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    updater.start_polling()
    updater.idle()

keep_alive()
main()
