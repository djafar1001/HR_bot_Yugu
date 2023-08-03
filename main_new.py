"""
HRБот– виртуальный ассистент предназначенный для коммуникации
с принятыми в Банк России на работу сотрудниками,
обученный общаться по ограниченному кругу сценариев
Бот обрабатывает команды:
start - запуск бота
edit - редактирует имя
continue - продолжение работы с ботом
help - информация о нахождении курсов

"""
from setings_HR import HR_BOT_TOKEN as TOKEN, BOT_MESSAGE as mess, HELP_MESS
import HR_Lib as lib

import telebot
from telebot import types
from os import path, remove

import pickle
from time import time, sleep

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду


class Employee:
    """Класс, представляющий нового сотрудника"""

    def __init__(self, name):
        self.name = name
        # self.training_start = lib.datetime.now()
        self.training_start = time()
        self.adaptation_dey = 1
        self.current_course = 1
        self.courses_completed = [0] * 5

    def info_time(self):
        time_begin = lib.format_time(self.training_start)
        print(time_begin, type(time_begin))
        print(self.training_start, type(self.training_start))

    def __str__(self):
        return f'Пользователь {self.name} начал адаптацию {lib.format_time(self.training_start)}' \
               f'сейчас изучает курс {self.current_course} всего изучено {str(self.courses_completed)}'


# Открываем или создаем словарь для хранения данных о сотрудниках
if path.exists('employees.db'):
    with open('employees.db', 'rb') as file:
        employees = pickle.load(file)
else:
    employees = {}


def dump_file():
    """Функция сохранения словаря пользователей в битный файл"""
    with open('employees.db', 'wb') as file:  # !!!нужно создать функцию
        pickle.dump(employees, file)


@bot.message_handler(commands=['start', 'help', 'continue', 'edit'])
def handle_start(message, employee=None):
    """
    После ввода команды /start Проверяем наличие пользователя в словаре сотрудников
    и в случае отсутствия запрашиваем его имя. Полученный результат передаем
    в функцию start_dialog

    :param message:
    :return:
    """
    if message.text == '/start':
        if message.chat.id not in employees.keys():
            bot.send_message(message.chat.id, mess[99][1])  # Приветствие
            with open('./pic/AnimatedSticker_hi.tgs', 'rb') as file:
                bot.send_sticker(message.chat.id, file)
            # Запрос имени сотрудника
            answer = bot.send_message(message.chat.id, mess[99][2])
            bot.register_next_step_handler(answer, start_dialog)
        else:
            employee = employees[message.chat.id]
            #       print(employee.__str__())
            #          bot.send_message(message.chat.id, employee.__str__())
            #       bot.send_message(message.chat.id, str(employee.courses_completed))

            if not all(employee.courses_completed):
                bot.send_message(message.chat.id, 'Давайте продолжим', reply_markup=lib.simple_menu())
            else:
                bot.send_message(message.chat.id, mess[0][8])
    elif message.text == '/help':
        help_m = bot.send_message(message.chat.id, HELP_MESS)
        sleep(12)
        bot.delete_message(message.chat.id, help_m.id)
    elif message.text in ['/continue', '/edit']:
        with open('./pic/Hand_work.tgs', 'rb') as file:
            ms_1 = bot.send_sticker(message.chat.id, file)
            ms_2 = bot.send_message(message.chat.id, 'Функционал в разработке')
            sleep(5)
            bot.delete_message(message.chat.id, ms_1.id)
            bot.delete_message(message.chat.id, ms_2.id)


def start_dialog(message):
    """
    Создание объекта сотрудника и сохранение его в словаре по
    идентификатору чата с последующей сериализацией в битовый файл.
    Выполняем диалог первого дня

    :param message:
    :return:
    """
    employee = Employee(message.text)
    employees[message.chat.id] = employee
    dump_file()  # Сохранение словаря сотрудников в файл

    bot.send_message(message.chat.id, f'Рад знакомству <b>{employee.name}</b>!\n{mess[99][3]}!', parse_mode='html')
    bot.send_message(message.chat.id, mess[0][7])

    bot.send_message(message.chat.id,
                     mess[0][4],
                     reply_markup=lib.simple_menu())

    @bot.callback_query_handler(func=lambda call: True)
    def pressing_reaction(call):
        if call.data == '1':
            if employee.current_course > 3:
                employee.adaptation_dey = 2
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text=f'<b>{employee.name}</b> {mess[employee.adaptation_dey][employee.current_course]}',
                                  parse_mode='html')
            bot.send_message(call.message.chat.id, mess[0][5],
                             reply_markup=lib.menu_ready(),
                             parse_mode='html')
        elif call.data == '0':
            time_out = bot.send_message(call.message.chat.id, mess[0][9])
            bot.delete_message(call.message.chat.id, call.message.id)
            sleep(10)
            bot.delete_message(call.message.chat.id, time_out.id)
            bot.send_message(call.message.chat.id,
                             mess[0][4],
                             reply_markup=lib.simple_menu())


@bot.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text.lower() == 'удалить' or message.text.lower() == 'elfkbnm':
        path_file = './bin/employees.db'
        try:
            remove(path_file)
        except:
            bot.send_message(message.chat.id, f'Файл {path_file} не найден')
    elif message.text == 'Прошел✔️':  # Реакция на нажатие кнопки "Прошел"

        employees[message.chat.id].courses_completed[employees[message.chat.id].current_course - 1] = 1
        employees[message.chat.id].current_course += 1

        if not all(employees[message.chat.id].courses_completed):
            with open('./pic/dog_.OK.tgs', 'rb') as file:
                dog_stiker = bot.send_sticker(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())
            sleep(3)
            bot.delete_message(message.chat.id, dog_stiker.id)

            bot.send_message(message.chat.id, mess[0][6],
                             reply_markup=lib.simple_menu())
        else:
            with open('./pic/Hand_.well_done.tgs', 'rb') as file:
                bot.send_sticker(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())

            bot.send_message(message.chat.id, mess[0][8])
    elif message.text.lower() == 'adm_sys':  # создает файл с информацией о пользователе
        lib.sys_info(employees)
        bot.send_message(message.chat.id, 'Файл создан')
        pass
    else:
        bot.send_message(message.chat.id, mess[0][10])  # сообщение бота на любой ввод не учтенный в коде


if __name__ == '__main__':
    print('Мой HR-бот')
    print(lib.format_time(time()))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')
