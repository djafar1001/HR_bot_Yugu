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
from setings_HR_new import HR_BOT_TOKEN as TOKEN, \
    BOT_MESSAGE as mess, \
    HELP_MESSAGE, QUESTIONS, QUEST_FIRST_LIST, QUEST_SECOND_LIST
import HR_Lib as lib

import telebot
from telebot import types
from os import path, remove

# import schedule
import pickle
# import datetime
from time import time, sleep

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду


class Employee:
    """Класс, представляющий параметры и функции сотрудника"""

    def __init__(self, name, id_user):
        self.name = name  # Имя пользователя
        self.id_user = id_user  # ID чата и пользователя
        # self.training_start = lib.datetime.now()
        self.training_start = time()  # Дата начала общения с чат-ботом в Unix от начала эпохи
        # self.training_start = lib.time_begin()  # Дата начала общения с чат-ботом
        self.adaptation_dey = 0  # Порядковый номер дня адаптации
        self.current_course = 1  # Номер текущего курса
        self.courses = [0] * 15  # Список курсов по порядку
        self.score_dey = [0] * 6  # Оценки первого дня поставленные пользователем
        self.score_second_dey = [0] * 3  # Оценка второго дня
        self.name_questionnaire = QUEST_FIRST_LIST
        self.second_quest = False
        self.check_score = 0  # Значение оценки для опросника (1-да, 0-нет)
        self.adaptation_completed = False  # параметр окончания адаптации
        self.index_question = 0  # Индекс вопросов в списке опросника

    def survey_first_day(self, id_mess, type_quest=1):
        """
        Функция опросника в первый рабочий день. Данные заносятся в self.score_dey
        да - 1, нет - 0 вопросы берутся из словаря questions файла setings_HR_new
        :return:
        """
        if self.index_question < len(self.name_questionnaire):
            if type_quest == 1:
                bot.edit_message_text(self.name_questionnaire[self.index_question],
                                      self.id_user,
                                      id_mess,
                                      reply_markup=lib.simple_menu('Yes_Q', 'No_Q'))
            else:
                answer = bot.send_message(self.id_user, self.name_questionnaire[self.index_question])
                bot.register_next_step_handler(answer, self.saving_results)
                pass
        else:
            try:
                bot.edit_message_text(mess[99][9],
                                      self.id_user,
                                      id_mess)
            except Exception:
                bot.send_message(self.id_user, mess[99][9])

            if self.adaptation_dey == 1:
                sleep(3)
                bot.edit_message_text(mess[99][10],
                                      self.id_user,
                                      id_mess)
            if any(self.score_second_dey):
                self.second_quest = True
            lib.dump_employees(employees)  # сериализация изменений объекта пользователя в файл
            self.index_question = 0
            self.adaptation_dey += 1
            # передаем управление ботом модулю schedule
            # schedule.every().day.until('09:00').do(notification_9_00, employees, message.chat.id)
            #
            # # временная замена schedule
            sleep(10)
            bot.send_message(self.id_user, f'======= Наступил {self.adaptation_dey} день адаптации======')
            notification_9_00(employees, self.id_user)

    def saving_results(self, message):
        self.score_second_dey[self.index_question] = message.text
        self.index_question += 1
        self.survey_first_day(message.id, type_quest=2)

    def begin_adapt(self):
        pass

    def info_time(self):
        time_begin = lib.format_time(self.training_start)
        print(time_begin, type(time_begin))
        print(self.training_start, type(self.training_start))

    def __str__(self):
        return f'Пользователь {self.name} начал адаптацию {lib.format_time(self.training_start)}' \
               f'сейчас изучает курс {self.current_course} всего изучено {str(self.courses)},' \
               f'опрос 1 дня {self.score_dey}'

    def test_message(self):
        """!!!ВРЕМЕННАЯ!!!Функция вывода тестового сообщения!!! """
        bot.send_message(self.id_user, '====message test====')
        bot.send_message(self.id_user, f'вопрос: {self.index_question}\n'
                                       f'id чата:{self.id_user}\n'
                         )


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

    bot.send_message(chat_id, '====09:00====')
    # ====================================
    bot.send_message(chat_id, f'{mess[1][1]} <b>{employee.name}!</b>',
                     parse_mode='html',
                     disable_notification=True)
    if employee.adaptation_dey == 1:
        bot.send_message(chat_id, mess[1][2], disable_notification=False)
        # sleep(3600)  # Действие в 10:00 первого дня
        sleep(6)
        bot.send_message(chat_id, '====10:00====')
        hr_phone = '+79876543210'  # телефон HR службы
        bot.send_message(chat_id,
                         f'{mess[1][3]} <a href="tel:{hr_phone}">{hr_phone}</a>',
                         parse_mode='HTML',
                         )
        # sleep(7200)  # Действие в 12:00 первого дня
        sleep(12)
        bot.send_message(chat_id, '====12:00====')

        bot.send_message(chat_id,
                         f'{employee.name}, {mess[1][4]}',
                         reply_markup=lib.simple_menu('Yes_HR', 'No_HR'),
                         disable_notification=True)
    elif employee.adaptation_dey == 2:
        bot.send_message(chat_id,
                         mess[99][2],
                         disable_notification=True,
                         reply_markup=lib.simple_menu())
    # elif employee.adaptation_dey == 3:
    else:
        bot.send_message(chat_id,
                         mess[99][4],
                         disable_notification=True,
                         reply_markup=lib.simple_menu())

        # ++++++++++++++++++++++++++++++++++++++++++++
        # bot.edit_message_text(mess[99][2],
        #                       chat_id,
        #                       inline_message_id=mess[99][9],
        #                       reply_markup=lib.simple_menu())
        pass
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
    with open('./pic/Wollfe_by.tgs', 'rb') as file:  # ************
        hi_stiker = bot.send_sticker(message.chat.id, file)  # Нужно сделать функцию
    sleep(3)
    # удаляем стикер и надпись прощания
    bot.delete_message(message.chat.id, hi_stiker.id)  # ************
    employee.adaptation_dey = 1

    # передаем управление ботом модулю shedule
    # schedule.every().day.until('09:00').do(notification_9_00, employees, message.chat.id)

    # ======временная замена schedule
    sleep(10)
    bot.edit_message_text('====Наступил 1 день адаптации====', message.chat.id, by_day.id)  # ************
    notification_9_00(employees, message.chat.id)
    # ======================================


def message_cours(chat_id):
    if employees[chat_id].current_course == 7 and not employees[chat_id].second_quest:
        employees[chat_id].name_questionnaire = QUEST_SECOND_LIST
        bot.send_message(chat_id,
                         mess[99][11],
                         reply_markup=lib.simple_menu(call_yes='yes_answer', call_no='no_answer')
                         )
    else:
        if employees[chat_id].adaptation_dey > 3:  # временное решение для отладки
            employees[chat_id].adaptation_dey = 3

        bot.send_message(chat_id=chat_id,
                         text=f'<b>{employees[chat_id].name}</b> '
                              f'{mess[employees[chat_id].adaptation_dey][employees[chat_id].current_course]}',
                         parse_mode='html'
                         )
        push_offer = bot.send_message(chat_id, mess[99][3],
                                      reply_markup=lib.menu_ready(),
                                      parse_mode='html')

        global id_message
        id_message = push_offer.id


@bot.callback_query_handler(func=lambda call: True)
def pressing_reaction(call):
    employee = employees[call.message.chat.id]  # Идентификация пользователя

    if call.data == 'yes':

        # bot.send_message(call.message.chat.id,
        #                  f'Имя пользователя:<b>{employee.name}</b>\n'
        #                  f'день адаптации:{employee.adaptation_dey}\n'
        #                  f'номер задания:{employee.current_course}\n'
        #                  f'название:{mess[employee.adaptation_dey][employee.current_course]}',
        #                  parse_mode='html')
        bot.delete_message(call.message.chat.id, call.message.id)
        message_cours(call.message.chat.id)
        # bot.edit_message_text(chat_id=call.message.chat.id,
        #                       message_id=call.message.id,
        #                       text=f'<b>{employee.name}</b> {mess[employee.adaptation_dey][employee.current_course]}',
        #                       parse_mode='html')
        # bot.send_message(call.message.chat.id, mess[99][3],
        #                  reply_markup=lib.menu_ready(),
        #                  parse_mode='html')
    # if call.data == 'yes':
    #     if employee.current_course > 3:
    #         employee.adaptation_dey = 2
    #     bot.edit_message_text(chat_id=call.message.chat.id,
    #                           message_id=call.message.id,
    #                           text=f'<b>{employee.name}</b> {mess[employee.adaptation_dey][employee.current_course]}',
    #                           parse_mode='html')
    #     bot.send_message(call.message.chat.id, mess[0][5],
    #                      reply_markup=lib.menu_ready(),
    #                      parse_mode='html')
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
        chif = bot.edit_message_text(mess[1][5], call.message.chat.id, call.message.id)

        # sleep(18000)    # установка таймера на 5 часа после сообщения
        sleep(8)
        bot.delete_message(call.message.chat.id, chif.id)
        bot.send_message(call.message.chat.id, '====17:00====')

        bot.send_message(call.message.chat.id,
                         mess[1][6],
                         reply_markup=lib.simple_menu(call_yes='yes_answer', call_no='no_answer'),
                         disable_notification=True)
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
        if employee.name_questionnaire == QUEST_FIRST_LIST:
            id_mess = bot.edit_message_text(mess[99][8], call.message.chat.id, call.message.id)
            employee.survey_first_day(id_mess.id)
        elif employee.name_questionnaire == QUEST_SECOND_LIST:
            id_mess = bot.edit_message_text(mess[99][12], call.message.chat.id, call.message.id)
            employee.survey_first_day(id_mess.id, type_quest=2)
            pass
    elif call.data == 'no_answer':
        element_develop(call.message.chat.id)
        pass
    #  'Yes_Q', 'No_Q' реакция на опрос первого дня
    elif call.data == 'Yes_Q':
        # employee.check_score = 1
        employee.score_dey[employee.index_question] = 1

        # employee.score_second_dey[employee.index_question] = int(call.message.text)
        employee.index_question += 1
        employee.survey_first_day(call.message.id)
    elif call.data == 'No_Q':
        # employee.check_score = 0
        employee.score_dey[employee.index_question] = 0
        employee.index_question += 1
        employee.survey_first_day(call.message.id)


@bot.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text.lower() == 'удалить' or message.text.lower() == 'elfkbnm':
        del_chat = employees.pop(message.chat.id, 'Такого чата в базе нет')
        bot.send_message(message.chat.id, del_chat, reply_markup=types.ReplyKeyboardRemove())


    # ========== Переделать с учетом изменения в словаре сообщений
    elif message.text == 'Прошел✔️':  # Реакция на нажатие кнопки "Прошел"

        employees[message.chat.id].courses[employees[message.chat.id].current_course - 1] = 1
        employees[message.chat.id].current_course += 1

        if not all(employees[message.chat.id].courses):
            with open('./pic/dog_.OK.tgs', 'rb') as file:
                dog_stiker = bot.send_sticker(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())

            lib.dump_employees(employees)  # сериализация изменений объекта пользователя в файл

            sleep(3)
            bot.delete_message(message.chat.id, dog_stiker.id)
            bot.delete_message(message.chat.id, id_message)
            message_cours(message.chat.id)

            # bot.send_message(message.chat.id, mess[0][6],
            #                  reply_markup=lib.simple_menu())
        else:
            with open('./pic/Hand_.well_done.tgs', 'rb') as file:
                bot.send_sticker(message.chat.id, file, reply_markup=types.ReplyKeyboardRemove())

            bot.send_message(message.chat.id, mess[99][5])
            lib.dump_employees(employees)
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
