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
if path.exists('employees.db'):
    with open('employees.db', 'rb') as file:
        employees = pickle.load(file)
else:
    employees = {}


@bot.message_handler(commands=['start'])
def handle_start(message, employee=None):
    """
    После ввода команды /start Проверяем наличие пользователя в словаре сотрудников
    и в случае отсутствия запрашиваем его имя. Полученный результат передаем
    в функцию start_dialog

    :param message:
    :return:
    """
    if message.chat.id not in employees.keys():
        bot.send_message(message.chat.id, 'Доброе утро! Я Вас приветствую в Банке России')
        # Запрос имени сотрудника
        answer = bot.send_message(message.chat.id, "Пожалуйста, укажите, как к Вам можно обращаться:")
        bot.register_next_step_handler(answer, start_dialog)
    else:
        if not all(employees[message.chat.id].courses_completed):
            bot.send_message(message.chat.id, 'Давайте продолжим')
        else:
            bot.send_message(message.chat.id, 'Вы успешно прошли все этапы адаптации'
                                              '\nУдачи в работе')




def start_dialog(message):
    """
    Создание объекта сотрудника и сохранение его в словаре по
    идентификатору чата с последующей сериализацией в битовый файл/
    Выполняем диалог первого дня

    :param message:
    :return:
    """
    employee = Employee(message.text)
    employees[message.chat.id] = employee

    with open('employees.db', 'wb') as file:
        pickle.dump(employees, file)

    bot.send_message(message.chat.id, f'{employee.name} с началом трудовой деятельности в Банке Росси')

    markup = types.InlineKeyboardMarkup(row_width=2)
    butt_yes = types.InlineKeyboardButton('Да', callback_data='1')
    butt_no = types.InlineKeyboardButton('Нет', callback_data='0')
    markup.add(butt_yes, butt_no)

    bot.send_message(message.chat.id,
                     f'{employee.name} Вы готовы приступить к работе по адаптации?',
                     reply_markup=markup)

# @bot.callback_query_handlers(func=lambda call: True):
# def reaktion(call):
#     pass


if __name__ == '__main__':
    print('Мой HR-бот')
    print(HR_Lib.format_time(4567824))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')
