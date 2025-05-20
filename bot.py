import os
import logging
import telebot
import openai

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Конфигурация клиента OpenAI через OpenRouter
openai_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Инициализация телеграм-бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я GigaVolchik 🐺 Спроси меня что угодно!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        response = openai_client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Можно менять модель (ниже список)
            messages=[
                {"role": "system", "content": "Ты дружелюбный и умный помощник."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

bot.polling()
