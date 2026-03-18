import os
import threading
import time
import telebot
import openai
from flask import Flask
# --- Настройки с переменных окружения (Secrets) ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_KEY
# --- Основная логика бота ---
@bot.message_handler(func=lambda msg: True)
def handle(msg):
    user_text = msg.text.strip()
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # можно заменить на 'gpt-4-turbo'
            messages=[{"role": "user", "content": user_text}],
            temperature=0.7
        )
        answer = completion.choices[0].message["content"]
        bot.reply_to(msg, answer)
    except Exception as e:
        bot.reply_to(msg, f"Ошибка: {e}")
# --- Flask-сервер для антизасыпания ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Бот работает!"
def run_flask():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    """Периодический пинг, чтобы Replit держал проект активным."""
    while True:
        time.sleep(300)
        try:
            import requests
            requests.get("[localhost](http://localhost:8080)")
        except Exception:
            pass
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    print("Бот запущен и слушает сообщения...")
    bot.polling(non_stop=True)