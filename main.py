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
# --- Flask-сервер для антизасыпания Render ---
# Создаем Flask-приложение, но не запускаем его web-сервер
app = Flask(__name__)
@app.route('/')
def home():
    return "Я рабочий бот!" # Можно поменять на любое приветствие
def run_flask_server():
    """Запускает Flask-сервер для Render'a."""
    port = int(os.environ.get("PORT", 8080)) # Render использует $PORT
    app.run(host="0.0.0.0", port=port)
# Запускаем Flask-сервер в отдельном потоке, чтобы он не блокировал бота
flask_thread = threading.Thread(target=run_flask_server)
flask_thread.daemon = True # Делаем поток фоновым
flask_thread.start()
# --- Логика самого Telegram-бота ---
# Здесь бот начинает опрашивать Telegram API
if __name__ == "__main__":
    print("Бот запущен и слушает сообщения...")
    bot.polling(non_stop=True)