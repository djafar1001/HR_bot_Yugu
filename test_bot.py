# import telebot
# import json
#
# from telebot import types
#
# # Создание экземпляра бота с использованием токена
# bot = telebot.TeleBot('YOUR_TELEGRAM_TOKEN')

from setings_HR import HR_BOT_TOKEN as TOKEN
import HR_Lib

import telebot
from telebot import types
from os import path
import json
import pickle
from datetime import datetime

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

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создание объекта сотрудника и сохранение его в словаре по идентификатору чата
    employee = Employee(message.chat.id)
    employees[message.chat.id] = employee

    # Отправка приветственного сообщения
    bot.reply_to(message, f"Привет, {employee.name}! Добро пожаловать на предприятие!")

    # Запрос имени сотрудника
    bot.send_message(message.chat.id, "Пожалуйста, укажите, как к вам можно обращаться:")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    if chat_id in employees:
        employee = employees[chat_id]

        if not employee.name:
            # Сохранение имени сотрудника
            employee.name = message.text

            # Отправка сообщения с поздравлением и ссылкой на документ
            bot.send_message(chat_id, f"Поздравляю с первым рабочим днем, {employee.name}!")
            bot.send_message(chat_id, "C началом трудовой деятельности в предприятии! "
                                      "Ознакомьтесь с документом по ссылке: <ссылка>")

            # Запрос на ввод курсов
            bot.send_message(chat_id, "Для эффективной работы рекомендуется пройти следующие вводные курсы:")
            bot.send_message(chat_id, "1. Курс 1: <ссылка>")
            bot.send_message(chat_id, "2. Курс 2: <ссылка>")
            # ...

        elif employee.courses_completed < 2:
            # Обработка завершения курса
            employee.courses_completed += 1

            # Отправка нового задания
            bot.send_message(chat_id, "Поздравляю с успешным завершением курса! "
                                      "Теперь приступите к следующему заданию.")

            # Отправка ссылки на следующий курс
            bot.send_message(chat_id, f"Курс {employee.courses_completed + 1}: <ссылка>")

            if employee.courses_completed == 2:
                # Вывод вопросника после второго дня
                send_questionnaire(chat_id)
        else:
            # Запрос обратной связи
            bot.send_message(chat_id, "Пожалуйста, оцените ваш прогресс в достижении цели 'Изучение предприятия' "
                                      "по шкале от 0 до 10:")
    else:
        # Обработка случая, когда сотрудник не зарегистрирован
        bot.send_message(chat_id, "Пожалуйста, начните с команды /start для регистрации на предприятии.")

# Обработчик инлайн-кнопок (ответов на вопросник)
@bot.callback_query_handler(func=lambda call: call.data.startswith('question_'))
def handle_questionnaire(call):
    chat_id = call.message.chat.id

    if chat_id in employees:
        employee = employees[chat_id]
        question_id = call.data.split('_')[1]

        if question_id not in employee.questionnaire:
            # Сохранение ответа на вопрос в словарь сотрудника
            employee.questionnaire[question_id] = int(call.data.split('_')[2])

            # Отправка следующего вопроса или благодарности за заполнение вопросника
            if len(employee.questionnaire) < 3:
                send_question(chat_id, len(employee.questionnaire) + 1)
            else:
                bot.send_message(chat_id, "Спасибо за заполнение вопросника!")

        # Сериализация данных о сотрудниках и сохранение в файл
        with open('employees.json', 'w') as file:
            json.dump(employees, file)

# Функция для отправки вопросника
def send_questionnaire(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 5

    for i in range(1, 11):
        button = types.InlineKeyboardButton(text=str(i), callback_data=f"question_1_{i}")
        markup.add(button)

    question = "1. Было ли вам комфортно работать с чатботом?"
    bot.send_message(chat_id, question, reply_markup=markup)

# Функция для отправки следующего вопроса
def send_question(chat_id, question_number):
    markup = types.InlineKeyboardMarkup(row_width=5)


    for i in range(1, 11):
        button = types.InlineKeyboardButton(text=str(i), callback_data=f"question_{question_number}_{i}")
        markup.add(button)

    if question_number == 2:
        question = "2. Материалы по работе в предприятии были понятными и доступными?"
    elif question_number == 3:
        question = "3. Оцените ваш прогресс в достижении цели 'Изучение предприятия' (от 0 до 10):"

    bot.send_message(chat_id, question, reply_markup=markup)

# Запуск бота
if __name__ == '__main__':
    print('Мой HR-бот')
    print(HR_Lib.format_time(4567824))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')