from setings_test import TOKEN_T_BOT as TOKEN
import Lib

import telebot
from telebot import types
#from os import path
#import json
#import pickle
#from datetime import datetime

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду


# Класс, представляющий нового сотрудника
class Employee:
    def __init__(self, name):
        self.name = name
        self.courses_completed = 0
        self.questionnaire = {}

# Словарь для хранения данных о сотрудниках
employees = {}
# Глобальный словарь для хранения оценок пользователя
user_ratings = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_ratings[user_id] = {}  # Инициализация словаря для оценок
    send_next_question(user_id)

def send_next_question(user_id):
    if user_id in user_ratings:
        # Проверяем, сколько вопросов уже задано
        num_questions_answered = len(user_ratings[user_id])
        if num_questions_answered < 10:  # Задаем максимум 10 вопросов
            question_number = num_questions_answered + 1
            question_text = f"Оцените вопрос {question_number} по 10-балльной шкале:"
            markup = create_inline_keyboard_2x5()
            bot.send_message(user_id, question_text, reply_markup=markup)
        else:
            calculate_and_send_average_rating(user_id)
    else:
        bot.send_message(user_id, "Опрос не найден. Начните с команды /start.")

def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=5)
    for i in range(1, 11):
        button = types.InlineKeyboardButton(str(i), callback_data=str(i))
        markup.add(button)
    return markup


def create_inline_keyboard_2x5():
    """
    Функция создает inline-меню из 10 кнопок в 2 ряда по 5 в каждом
    с соответствущим числом и callbeck = этому числу в str
    """
    markup = types.InlineKeyboardMarkup()

    row1 = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 6)]
    row2 = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(6, 11)]

    markup.row(*row1)  # Первый ряд
    markup.row(*row2)  # Второй ряд

    return markup


@bot.callback_query_handler(func=lambda call: call.data in [str(i) for i in range(1, 11)])
def callback_handler(call):
    user_id = call.message.chat.id
    if user_id in user_ratings:
        current_question_number = len(user_ratings[user_id]) + 1
        rating = int(call.data)
        user_ratings[user_id][current_question_number] = rating
        send_next_question(user_id)
        # Удаление сообщения с предыдущим вопросом и InlineKeyboard
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Вы поставили оценку: {rating}")
    else:
        bot.send_message(user_id, "Опрос не найден. Начните с команды /start.")

def calculate_and_send_average_rating(user_id):
    if user_id in user_ratings:
        ratings = user_ratings[user_id].values()
        average_rating = sum(ratings) / len(ratings)
        bot.send_message(user_id, f"Средний балл: {average_rating:.2f}")
        # Очистка данных об оценках
        del user_ratings[user_id]



# Запуск бота
if __name__ == '__main__':
    print('Мой HR-бот')
    print(Lib.format_time(4567824))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')