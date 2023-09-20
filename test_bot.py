from setings_test import TOKEN_T_BOT as TOKEN
import telebot
import HR_Lib
#from telebot import types
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



# Запуск бота
if __name__ == '__main__':
    print('Мой HR-бот')
    print(HR_Lib.format_time(4567824))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')