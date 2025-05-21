import os
import logging
import openai
import telebot

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Получение токенов и модели из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "huggingfaceh4/zephyr-7b-beta")  # можно заменить на другую модель

# Проверка токенов
if not TELEGRAM_BOT_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("Переменные окружения TELEGRAM_BOT_TOKEN и OPENROUTER_API_KEY должны быть заданы.")

# Настройка клиента OpenRouter
openai.api_key = OPENROUTER_API_KEY
openai.base_url = "https://openrouter.ai/api/v1"  # важно!

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я GigaVolchik 🐺 Можешь написать мне любой вопрос!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

bot.polling()
