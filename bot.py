import os
import telebot

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN не найден")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот работает ✅")

print("Bot started...")
bot.infinity_polling()
