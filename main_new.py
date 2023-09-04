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
from setings_HR_new import HR_BOT_TOKEN as TOKEN, BOT_MESSAGE as mess, HELP_MESSAGE, QUESTIONS
import HR_Lib as lib

import telebot
from telebot import types
from os import path, remove

import schedule
import pickle
import datetime
from time import time, sleep

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду


class Employee:
    """Класс, представляющий параметры и функции сотрудника"""

    def __init__(self, name, id_user):
        self.name = name  # Имя пользователя
        self.id_user = id_user # ID сата и пользователя
        # self.training_start = lib.datetime.now()
        self.training_start = time()  # Дата начала общения с чат-ботом в Unix от начала эпохи
        #self.training_start = lib.time_begin()  # Дата начала общения с чат-ботом
        self.adaptation_dey = 0  # Порядковый номер дня адаптации
        self.current_course = 0  # Номер текущего курса
        self.courses = [0] * 14  # Список курсов по порядку
        self.score_dey = [0] * 6  # Оценки первого дня поставленные пользователем
        self.check_score = 0
        self.adaptation_completed = False

#  Копия функции для попытки аптимизмции
#     def questionnaire_first_day(self, id_chat):
#         """
#         Функция опросника в первый рабочий день. Данные заносятся в self.score_dey
#         да - 1, нет - 0 вопросы берутся из словаря questions файла setings_HR_new
#         :return:
#         """
#         info_quest = bot.send_message(id_chat, mess[99][8])
#
#
#         for i_index, i_quest in QUESTIONS.items():
#             question = bot.send_message(id_chat,
#                                         i_quest,
#                                         reply_markup=lib.simple_menu('Yes_Q', 'No_Q'))
#             sleep(5)
#             #bot.send_message(id_chat, str(self.check_score))
#             self.score_dey[i_index - 1] = self.check_score
#             bot.delete_message(id_chat, question.id)
#
#         bot.send_message(id_chat, mess[99][9])
    def questionnaire_first_day(self):
        """
        Функция опросника в первый рабочий день. Данные заносятся в self.score_dey
        да - 1, нет - 0 вопросы берутся из словаря questions файла setings_HR_new
        :return:
        """
        bot.send_message(self.id_user, mess[99][8])

        for i_index, i_quest in QUESTIONS.items():
            question = bot.send_message(self.id_user,
                                        i_quest,
                                        reply_markup=lib.simple_menu('Yes_Q', 'No_Q'))
            sleep(5)
            #bot.send_message(id_chat, str(self.check_score))
            self.score_dey[i_index - 1] = self.check_score
            bot.delete_message(self.id_user, question.id)

        bot.send_message(self.id_user, mess[99][9])
        # self.adaptation_dey = 2
        # # передаем управление ботом модулю shedule
        # # schedule.every().day.until('09:00').do(notification_9_00, employees, message.chat.id)
        #
        # # временная замена schedule
        # sleep(20)
        # bot.send_message(message.chat.id, '======= Наступил 1 день адаптации======')
        # notification_9_00(employees, message.chat.id)
        # # ======================================
    def begin_adapt(self):


    def info_time(self):
        time_begin = lib.format_time(self.training_start)
        print(time_begin, type(time_begin))
        print(self.training_start, type(self.training_start))

    def __str__(self):
        return f'Пользователь {self.name} начал адаптацию {lib.format_time(self.training_start)}' \
               f'сейчас изучает курс {self.current_course} всего изучено {str(self.courses)},' \
               f'опрос 1 дня {self.score_dey}'


# Открываем или создаем словарь для хранения данных о сотрудниках
if path.exists('./data/employees.db'):
    with open('./data/employees.db', 'rb') as file:
        employees = pickle.load(file)
else:
    employees = {}

# Требуется создания функции проверки состояния процесса адаптации для всех пользователей

# ==============================================
def request_adaptation():
    pass



def element_develop(chat_id):
    """
    Функция заглушка на неработающие элементы
    :return:
    """
    with open('./pic/Hand_work.tgs', 'rb') as file:
        ms_1 = bot.send_sticker(chat_id, file)
        ms_2 = bot.send_message(chat_id, 'Функционал в разработке')
        sleep(5)
        bot.delete_message(chat_id, ms_1.id)
        bot.delete_message(chat_id, ms_2.id)
# ==============================================

def notification_9_00(employees_dict, chat_id):
    """
    Функция направляет push-сообщение пользователю для начала работы
    :param employees_dict:
    :param chat_id:
    :return:
    """
    employee = employees_dict[chat_id]
    # Временная надпись о смене дня
    # n_dey = bot.send_message(chat_id, f'{employee.adaptation_dey} день адаптации')
    # bot.delete_message(chat_id, n_dey.id)
    bot.send_message(chat_id, '====09:00====')
    # ====================================
    bot.send_message(chat_id, f'{mess[1][1]} {employee.name}!', disable_notification=True)
    if employee.adaptation_dey == 1:
        bot.send_message(chat_id, mess[1][2])
        # sleep(3600)  # Действие в 10:00 первого дня
        sleep(5)
        bot.send_message(chat_id, '====10:00====')
        hr_phone = '+79876543210'
        bot.send_message(chat_id,
                         f'{mess[1][3]} <a href="tel:{hr_phone}">{hr_phone}</a>',
                         parse_mode='HTML',
                         disable_notification=True, )
        bot.send_message(chat_id, '====12:00====')
        sleep(12)
        bot.send_message(chat_id,
                         f'{employee.name}, {mess[1][4]}',
                         reply_markup=lib.simple_menu('Yes_HR', 'No_HR'), timeout=10)


    #  lib.day_score(employee)  # Оценка дня

    pass


@bot.message_handler(commands=['start', 'help', 'continue', 'edit'])
def handle_start(message):
    """
    После ввода команды /start Проверяем наличие пользователя в словаре сотрудников
    и в случае отсутствия запрашиваем его имя. Полученный результат передаем
    в функцию start_dialog

    :param message:
    :return:
    """
    if message.text == '/start':
        if message.chat.id not in employees.keys():
            bot.send_message(message.chat.id, mess[0][2])  # Приветствие
            with open('./pic/AnimatedSticker_hi.tgs', 'rb') as file:
                bot.send_sticker(message.chat.id, file)
            # Запрос имени сотрудника
            answer = bot.send_message(message.chat.id, mess[0][3])
            bot.register_next_step_handler(answer, start_dialog)
        else:
            #  ?????
            # Подгружаем из словаря пользователей объект текущего пользователя в переменную
            # В случае отсутствия (что мало вероятно) предлогам нажать start
            employee = employees.get(message.chat.id, 'Нажмите еще раз команду меню /start')
            #       print(employee.__str__())
            #          bot.send_message(message.chat.id, employee.__str__())
            #       bot.send_message(message.chat.id, str(employee.courses_completed))

#            if not all(employee.courses):
            if employee.adaptation_completed:
                bot.send_message(message.chat.id, mess[99][5])
            else:
                bot.send_message(message.chat.id, 'Давайте продолжим', reply_markup=lib.simple_menu())



    elif message.text == '/help':
        help_m = bot.send_message(message.chat.id, HELP_MESSAGE)
        sleep(12)
        bot.delete_message(message.chat.id, help_m.id)
    elif message.text in ['/continue', '/edit']:
        element_develop(message.chat.id)
        # with open('./pic/Hand_work.tgs', 'rb') as file:
        #     ms_1 = bot.send_sticker(message.chat.id, file)
        #     ms_2 = bot.send_message(message.chat.id, 'Функционал в разработке')
        #     sleep(5)
        #     bot.delete_message(message.chat.id, ms_1.id)
        #     bot.delete_message(message.chat.id, ms_2.id)


def start_dialog(message):
    """
    Создание объекта сотрудника и сохранение его в словаре по
    идентификатору чата с последующей сериализацией в битовый файл.
    Выполняем диалог первого дня

    :param message:
    :return:
    """
    employee = Employee(message.text, message.chat.id)
    employees[message.chat.id] = employee
    lib.dump_employees(employees)  # Сохранение изменения словаря в файл

    bot.send_message(message.chat.id, f'Рад знакомству <b>{employee.name}</b>!\n{mess[0][1]}!', parse_mode='html')
    bot.send_message(message.chat.id, mess[0][4])
    sleep(5)
    by_day = bot.send_message(message.chat.id, mess[0][6])

    # Сткер прощания
    with open('./pic/Wollfe_by.tgs', 'rb') as file:          # ************
        hi_stiker = bot.send_sticker(message.chat.id, file)  # Нужно сделать функцию
    sleep(10)
    # удаляем стикер и надпись прощания
    bot.delete_message(message.chat.id, hi_stiker.id)                         # ************
    bot.edit_message_text('========+++++======', message.chat.id, by_day.id)  # ************

    employee.adaptation_dey = 1
    # передаем управление ботом модулю shedule
    #schedule.every().day.until('09:00').do(notification_9_00, employees, message.chat.id)

    # временная замена schedule
    sleep(20)
    bot.send_message(message.chat.id, '======= Наступил 1 день адаптации======')
    notification_9_00(employees, message.chat.id)
    # ======================================


@bot.callback_query_handler(func=lambda call: True)
def pressing_reaction(call):
    employee = employees[call.message.chat.id]  # Идентификация пользователя

    if call.data == 'yes':
        if employee.current_course > 3:
            employee.adaptation_dey = 2
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text=f'<b>{employee.name}</b> {mess[employee.adaptation_dey][employee.current_course]}',
                              parse_mode='html')
        bot.send_message(call.message.chat.id, mess[0][5],
                         reply_markup=lib.menu_ready(),
                         parse_mode='html')
    elif call.data == 'no':
        time_out = bot.send_message(call.message.chat.id, mess[0][9])
        bot.delete_message(call.message.chat.id, call.message.id)
        sleep(10)
        bot.delete_message(call.message.chat.id, time_out.id)
        bot.send_message(call.message.chat.id,
                         mess[0][4],
                         reply_markup=lib.simple_menu())
    # 'Yes_HR','No_HR' реакция о вопросе про документы
    elif call.data == 'Yes_HR':
        bot.send_message(call.message.chat.id, mess[1][5])

        sleep(5)                                                 # установка таймера на 4 часа после сообщения
        bot.send_message(call.message.chat.id, '====Прошло 4 часа====')  # 14 400 сек =============================

        bot.send_message(call.message.chat.id,
                         mess[1][6],
                         reply_markup=lib.simple_menu(call_yes='yes_answer', call_no='no_answer'))
    elif call.data == 'No_HR':
        time_out = bot.send_message(call.message.chat.id, mess[99][6])
        sleep(5)
        bot.delete_message(call.message.chat.id, time_out.id - 1)
        bot.delete_message(call.message.chat.id, time_out.id)
        sleep(10)
        bot.send_message(call.message.chat.id,
                         f'{employee.name}, {mess[1][4]}',
                         reply_markup=lib.simple_menu('Yes_HR', 'No_HR'))
    # 'yes_answer', 'no_answer' реакция на приглашение к опросу
    elif call.data == 'yes_answer':
        employee.questionnaire_first_day()

    elif call.data == 'no_answer':
        element_develop(call.message.chat.id)
        pass
    #  'Yes_Q', 'No_Q' реакция на опрос первого дня
    elif call.data == 'Yes_Q':
        employee.check_score = 1
    elif call.data == 'No_Q':
        employee.check_score = 0


@bot.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text.lower() == 'удалить' or message.text.lower() == 'elfkbnm':
        path_file = './data/employees.db'
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
