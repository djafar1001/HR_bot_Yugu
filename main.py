"""
HRБот– виртуальный ассистент предназначенный для коммуникации
с принятыми в Банк России на работу сотрудниками,
обученный общаться по ограниченному кругу сценариев
"""
from setings_HR import HR_BOT_TOKEN as TOKEN, BOT_MESSSAGE as mess
import HR_Lib as lib

import telebot
from telebot import types
from os import path, remove

import pickle
from time import time, sleep

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду


# Класс, представляющий нового сотрудника
class Employee:
    def __init__(self, name):
        self.name = name
#        self.training_start = datetime.now()
        self.training_start = time()
        self.current_course = 0
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
        bot.send_message(message.chat.id, mess[0][0])
        # Запрос имени сотрудника
        answer = bot.send_message(message.chat.id, mess[0][1])
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

    bot.send_message(message.chat.id, f'Рад знакомству {employee.name}!\n{mess[1][0]}!')
    #    bot.send_message(message.chat.id, f'{employee.name} с началом трудовой деятельности в Банке Росси')

    # markup = types.InlineKeyboardMarkup(row_width=2)
    # butt_yes = types.InlineKeyboardButton('Да', callback_data='1')
    # butt_no = types.InlineKeyboardButton('Нет', callback_data='0')
    # markup.add(butt_yes, butt_no)

    # bot.send_message(message.chat.id,
    #                  f'{employee.name} Вы готовы приступить к работе по адаптации?',
    #                  reply_markup=lib.simple_menu())
    bot.send_message(message.chat.id,
                     mess[1][1],
                     reply_markup=lib.simple_menu())

    @bot.callback_query_handler(func=lambda call: True)
    def pressing_reaction(call):
        if call.data == '1':
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text=f'{employee.name}  {mess[1][2]}')
            bot.send_message(call.message.chat.id, mess[1][3],
                             reply_markup=lib.menu_ready())
        else:
            ...

@bot.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text == 'удалить':
        path_file = 'employees.db'
        try:
            remove(path_file)
        except:
            bot.send_message(message.chat.id,f'Файл {path_file} не найден')
    elif message.text == 'Прошел✔️':

        employees[message.chat.id].courses_completed[employees[message.chat.id].current_course] = 1
        employees[message.chat.id].current_course += 1

        bot.send_message(message.chat.id, mess[1][4],
                         reply_markup=lib.simple_menu())



if __name__ == '__main__':
    print('Мой HR-бот')
    print(lib.format_time(time()))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')
