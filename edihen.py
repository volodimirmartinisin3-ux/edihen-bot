import telebot
from groq import Groq
import os


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_KEY)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я AI-асистент. Постав будь-яке питання 🤖")

@bot.message_handler(func=lambda message: True)
def ask_ai(message):
    bot.send_message(message.chat.id, "Думаю... ⏳")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Ти — асистент на ім'я Тарас. Відповідай тільки українською мовою."},
            {"role": "user", "content": message.text}
        ]
    )

    answer = response.choices[0].message.content
    bot.send_message(message.chat.id, answer)

bot.polling()
