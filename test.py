import telebot
from telebot import types

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# Глобальный словарь для хранения текущего вопроса для каждого пользователя
current_question = {}

# Вопросы для опроса
questions = [
    "Вопрос 1: Рабочее место было организовано?",
    "Вопрос 2: Почта подключена?",
    "Вопрос 3: Удалось познакомиться с твоей командой?",
    "Вопрос 4: Ты передал все документы для оформления в hr-службу?",
    "Вопрос 5: Понятно ли, где можно пообедать?",
    "Вопрос 6: Ты ознакомился с рабочим графиком?"
]

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    current_question[user_id] = 0  # Инициализация текущего вопроса
    send_current_question(user_id)

def send_current_question(user_id):
    if user_id in current_question:
        question_index = current_question[user_id]
        if question_index < len(questions):
            question_text = questions[question_index]
            markup = create_inline_keyboard()
            bot.send_message(user_id, question_text, reply_markup=markup)
        else:
            bot.send_message(user_id, "Опрос завершен.")
    else:
        bot.send_message(user_id, "Опрос не найден. Начните с команды /start.")

def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton("Да", callback_data="yes")
    no_button = types.InlineKeyboardButton("Нет", callback_data="no")
    markup.add(yes_button, no_button)
    return markup

@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def callback_handler(call):
    user_id = call.message.chat.id
    if user_id in current_question:
        question_index = current_question[user_id]
        if question_index < len(questions):
            current_question[user_id] += 1  # Переходим к следующему вопросу
            send_current_question(user_id)
            # Удаление сообщения с предыдущим вопросом и InlineKeyboard
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ваш ответ: " + call.data)
    else:
        bot.send_message(user_id, "Опрос не найден. Начните с команды /start.")

bot.polling()
