"""
HRБот– виртуальный ассистент предназначенный для коммуникации
с принятыми в Банк России на работу сотрудниками,
обученный общаться по ограниченному кругу сценариев
"""
from setings_HR import HR_BOT_TOKEN as TOKEN
import HR_Lib

import telebot
from telebot import types

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



# Словарь для хранения данных о сотрудниках
employees = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создание объекта сотрудника и сохранение его в словаре по идентификатору чата
    employee = Employee(message.chat.id)
    employees[message.chat.id] = employee







if __name__ == '__main__':
    print('Мой HR-бот')
    print(HR_Lib.format_time(4567824))

