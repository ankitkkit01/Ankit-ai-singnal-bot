from flask import Flask from threading import Thread import requests import time from telegram.ext import Updater, CommandHandler

app = Flask('')

@app.route('/') def home(): return "I'm alive!"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive(): t = Thread(target=run) t.start()

TELEGRAM_BOT_TOKEN = '7413469925:AAGfVC48BAAilkOO_yk-li2v6xg9duG2inU' TELEGRAM_CHAT_ID = '6065493589'

closing_prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41, 46.22, 45.64, 46.21]

def send_telegram_message(message): url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage' payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message} requests.post(url, data=payload)

def start(update, context): context.bot.send_message(chat_id=update.effective_chat.id, text="Signal service started!") while True: message = f"Trading Signal:\nPrice: {closing_prices[-1]}\nSignal: BUY (RSI below 30)" send_telegram_message(message) time.sleep(180)

def stop(update, context): context.bot.send_message(chat_id=update.effective_chat.id, text="Signal service stopped!") exit(0)

def main(): updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("start", start)) dp.add_handler(CommandHandler("stop", stop)) updater.start_polling() updater.idle()

keep_alive() main()
