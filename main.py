"""
HRБот– виртуальный ассистент предназначенный для коммуникации
с принятыми в Банк России на работу сотрудниками,
обученный общаться по ограниченному кругу сценариев
"""
from setings_HR import HR_BOT_TOKEN as TOKEN
import HR_Lib

import telebot
from telebot import types
from os import path
import pickle
from datetime import datetime

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду


# Класс, представляющий нового сотрудника
class Employee:
    def __init__(self, name):
        self.name = name
        self.training_start = datetime.now()
        self.courses_completed = [0] * 5


# Открываем или создаем словарь для хранения данных о сотрудниках
if path.exists('employees.dt'):
    with open('employees.dt', 'rb', encoding='utf-8') as file:
        employees = pickle.load(file)
else:
    employees = {}


@bot.message_handler(commands=['start'])
def handle_start(message, employee=None):
    # Создание объекта сотрудника и сохранение его в словаре по идентификатору чата
    if message.chat.id not in employees.keys():
        bot.send_message(message.chat.id, 'Доброе утро! Я Вас приветствую в Банке России')
        # Запрос имени сотрудника
        bot.send_message(message.chat.id, "Пожалуйста, укажите, как к Вам можно обращаться:")

        employee = Employee(message.text)
        employees[message.chat.id] = employee
        bot .send_message(message.chat.id, f'{employee.name} с началом трудовой деятельности в Банке Росси')
    else:
        ...

        bot .send_message(message.chat.id, f'{employee.name} Вы готовы приступить к работе по адаптации?')










if __name__ == '__main__':
    print('Мой HR-бот')
    print(HR_Lib.format_time(4567824))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)
    with open('employees.dt', 'wb', encoding='utf-8') as file:
        pickle.dump(employees)
    print('Stoped')
