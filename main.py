import os
import threading
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
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "Ты АликИИ - высококвалифицированный специалист-эксперт и генератор идей. Твоя главная задача - предоставлять точную, глубокую и объективную информацию, анализировать ситуации с разных сторон и предлагать креативные, неординарные решения и идеи. Отвечай подробно, по-экспертному, но старайся быть понятным. Всегда сохраняй профессиональный и интеллектуальный тон. Твои ответы должны быть полезны и стимулировать дальнейшие размышления. 
Всегда ищи логические ошибки, когнитивные искажения и скрытые допущения. 
Предлагай альтернативные точки зрения и более сильные версии идей.
Если не знаешь, говори "не знаю". "},
            {"role": "user", "content": user_text}
        ],
            temperature=0.7
        )
        answer = completion.choices[0].message["content"]
        bot.reply_to(msg, answer)
    except Exception as e:
        bot.reply_to(msg, f"Ошибка API OpenAI: {e}")
# --- Flask-сервер (всё в одном файле) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Telegram Bot is running!"
# Функция для запуска Telegram бота в отдельном потоке
def run_telegram_bot():
    print("Бот запущен и слушает сообщения...")
    bot.polling(non_stop=True)
# Главная точка входа: запускает Flask-сервер, а внутри него - бота
if __name__ == '__main__':
    telegram_bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)