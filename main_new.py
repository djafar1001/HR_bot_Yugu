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
    HELP_MESSAGE, QUEST_FIRST_LIST, QUEST_SECOND_LIST, ADM_MESS, TEXT_QUESTIONNAIRES
# from HR_Lib.class_user import Employee
import HR_Lib as lib
import HR_Lib.keyboard as kb  # вызов модуля организации меню

import telebot
from telebot import types
from os import path, remove

# import schedule
import pickle
# import datetime
from time import time, sleep

from loguru import logger

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду

global employee
logger.add()

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
        self.lost_message = None
        self.id_hi = 0  # индекс стикера приветствия
        self.survey_days = [3, 4, 5, 30, 60, 90]  # Список дней в которые проводятся текстовые опросы
        self.survey_next = [9, 10, 11]  # Список курсов перед которыми проводятся текстовые опросы
        self.quest_rez = {}

    def survey_first_day(self, id_mess, type_quest=1):
        """
        Функция опросника в первый рабочий день. Данные заносятся в self.score_dey
        да - 1, нет - 0 вопросы берутся из списка QUEST_FIRST_LIST файла setings_HR_new
        :return: None
        """
        if self.index_question < len(self.name_questionnaire):
            if type_quest == 1:
                bot.edit_message_text(self.name_questionnaire[self.index_question],
                                      self.id_user,
                                      id_mess,
                                      reply_markup=kb.simple_menu('Yes_Q', 'No_Q'))
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
            self.adaptation_dey += 1  # 3 день
            # передаем управление ботом модулю schedule
            # schedule.every().day.until('09:00').do(notification_9_00, employees, message.chat.id)
            #
            # # временная замена schedule
            sleep(5)
            bot.send_message(self.id_user, f'======= Наступил {self.adaptation_dey} день адаптации======')
            bot.delete_message(self.id_user, self.id_hi)
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
if path.exists('Employee/employees.pkl'):
    with open('Employee/employees.pkl', 'rb') as file:
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
    # employee = employees_dict[chat_id]

    bot.send_message(chat_id, '====09:00====')
    # ====================================
    bot.send_message(chat_id, f'{mess[1][1]} <b>{employee.name}!</b>',
                     parse_mode='html',
                     disable_notification=True)
    stiker_hi(chat_id)
    if employee.adaptation_dey == 1:
        bot.send_message(chat_id, mess[1][2], disable_notification=False)
        # sleep(3600)  # Действие в 10:00 первого дня
        sleep(3)
        bot.send_message(chat_id, '====10:00====')
        hr_phone = '+79876543210'  # телефон HR службы
        bot.send_message(chat_id,
                         f'{mess[1][3]} <a href="tel:{hr_phone}">{hr_phone}</a>',
                         parse_mode='HTML',
                         )
        # sleep(7200)  # Действие в 12:00 первого дня
        sleep(5)
        bot.send_message(chat_id, '====12:00====')

        bot.send_message(chat_id,
                         f'{employee.name}, {mess[1][4]}',
                         reply_markup=kb.simple_menu('Yes_HR', 'No_HR'),
                         disable_notification=True)
    elif employee.adaptation_dey == 2:
        bot.send_message(chat_id,
                         mess[99][2],
                         disable_notification=True,
                         reply_markup=kb.simple_menu())
    # elif employee.adaptation_dey == 3:
    #     bot.send_message(chat_id,
    #                      mess[99][4],
    #                      disable_notification=True,
    #                      reply_markup=lib.simple_menu())
    #
    else:
        bot.send_message(chat_id,
                         mess[99][4],
                         disable_notification=True,
                         reply_markup=kb.simple_menu())


def stiker_hi(chat_id):
    """Функция выводит стикер приветствия"""
    with open('./pic/AnimatedSticker_hi.tgs', 'rb') as file:
        id_mess = bot.send_sticker(chat_id, file)
    try:
        employees[chat_id].id_hi = id_mess.id
    except KeyError:
        return id_mess.id


def send_next_question():
    """
    Функция направляет очередной вопрос из списка по ключу равному номеру дня адаптации
    """
    if employee.index_question < len(employee.name_questionnaire[employee.adaptation_dey]):
        query = bot.send_message(employee.id_user, f'Вопрос {employee.index_question + 1}\n'
                                                   f'{employee.name_questionnaire[employee.adaptation_dey][employee.index_question]}')
        bot.register_next_step_handler(query, save_query)
    else:
        bot.send_message(employee.id_user, 'Спасибо за пройденный опрос')
        employee.index_question = 0
        lib.dump_employees(employees)
        employee.adaptation_dey += 1

        if employee.adaptation_dey < 6:
            sleep(5)
            bot.send_message(employee.id_user, f'==== Наступил {employee.adaptation_dey} день адаптации===')
            bot.delete_message(employee.id_user, employee.id_hi)

        notification_9_00(employees, employee.id_user)
        # ===========================
        # if employee.survey_days:
        #     continue_quest()
        # else:
        #     bot.send_message(employee.id_user, f'quest_rez={employee.quest_rez}')
        #     bot.send_message(employee.id_user, 'Тестирование закончено')


def save_query(message):
    """
    Функция сохраняет ответ пользователя в список ответов,
    привязанный к ключу дня адаптации, в соответствии с индексом вопросов
    И выполняет запуск функции вывода очередного вопроса
    """
    employee.quest_rez[employee.adaptation_dey].append(message.text)
    employee.index_question += 1
    send_next_question()


@bot.message_handler(commands=['start', 'help', 'continue', 'edit', 'adm'])
def handle_start(message: types.Message):
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
            global mess_hi
            mess_hi = stiker_hi(message.chat.id)
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
                bot.send_message(message.chat.id,
                                 mess[99][4],
                                 reply_markup=kb.simple_menu())

    elif message.text == '/help':
        help_m = bot.send_message(message.chat.id, HELP_MESSAGE)
        sleep(5)
        bot.delete_message(message.chat.id, help_m.id)
    elif message.text in ['/continue', '/edit']:
        element_develop(message.chat.id)
        # with open('./pic/Hand_work.tgs', 'rb') as file:
        #     ms_1 = bot.send_sticker(message.chat.id, file)
        #     ms_2 = bot.send_message(message.chat.id, 'Функционал в разработке')
        #     sleep(5)
        #     bot.delete_message(message.chat.id, ms_1.id)
        #     bot.delete_message(message.chat.id, ms_2.id)
    elif message.text.lower() == '/adm':  # Административное меню
        bot.send_message(message.chat.id,
                         ADM_MESS,
                         parse_mode='html')
        pass


def start_dialog(message: types.Message):
    """
    Создание объекта сотрудника и сохранение его в словаре по
    идентификатору чата с последующей сериализацией в битовый файл.
    Выполняем диалог первого дня

    :param message:
    :return:
    """
    # co-worker
    global employee
    employee = Employee(message.text, message.chat.id)
    employees[message.chat.id] = employee
    lib.dump_employees(employees)  # Сохранение изменения словаря в файл
    employee.id_hi = mess_hi

    bot.send_message(message.chat.id, f'Рад знакомству <b>{employee.name}</b>!\n{mess[0][1]}!',
                     parse_mode='html')
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
    sleep(7)

    bot.delete_message(message.chat.id, employees[message.chat.id].id_hi)  # удаление стикера приветствия
    bot.edit_message_text('====Наступил 1 день адаптации====', message.chat.id, by_day.id)  # ************
    notification_9_00(employees, message.chat.id)
    # ======================================


def message_cours(chat_id):
    """"
    """
    if employees[chat_id].current_course == 7 and not employees[chat_id].second_quest:
        employees[chat_id].name_questionnaire = QUEST_SECOND_LIST
        bot.send_message(chat_id,
                         f'<b>{employees[chat_id].name}</b> {mess[99][11]}',
                         reply_markup=kb.simple_menu(call_yes='yes_answer', call_no='no_answer'),
                         parse_mode='html'
                         )
    elif employees[chat_id].adaptation_dey in employees[chat_id].survey_days \
            and employees[chat_id].current_course in employees[chat_id].survey_next:
        #        if employees[chat_id].current_course == employees[chat_id].survey_next.pop(0):
        employees[chat_id].name_questionnaire = TEXT_QUESTIONNAIRES
        employees[chat_id].survey_next.pop(0)
        if employees[chat_id].adaptation_dey == 5:
            mess_survey = f'<b>{employees[chat_id].name}</b> {mess[99][15]}'
        else:
            mess_survey = f'<b>{employees[chat_id].name}</b> {mess[99][14]}'
        bot.send_message(chat_id,
                         mess_survey,
                         reply_markup=kb.simple_menu(call_yes='yes_answer', call_no='no_answer'),
                         parse_mode='html'
                         )
        pass
    else:
        if employees[chat_id].adaptation_dey > 6:  # временное решение для отладки
            employees[chat_id].adaptation_dey = 6
        if employees[chat_id].current_course == 1:
            bot.send_message(chat_id, mess[0][5])
            sleep(3)
        bot.send_message(chat_id=chat_id,
                         text=f'<b>{employees[chat_id].name}</b> '
                              f'{mess[employees[chat_id].adaptation_dey][employees[chat_id].current_course]}',
                         parse_mode='html'
                         )
        push_offer = bot.send_message(chat_id, mess[99][3],
                                      reply_markup=kb.menu_ready(),
                                      parse_mode='html')

        global id_message
        id_message = push_offer.id


@bot.callback_query_handler(func=lambda call: True)
def pressing_reaction(call: types.CallbackQuery):
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
    # if call.Employee == 'yes':
    #     if employee.current_course > 3:
    #         employee.adaptation_dey = 2
    #     bot.edit_message_text(chat_id=call.message.chat.id,
    #                           message_id=call.message.id,
    #                           text=f'<b>{employee.name}</b> {mess[employee.adaptation_dey][employee.current_course]}',
    #                           parse_mode='html')
    # !!!! Найти место для вывода,
    #     bot.send_message(call.message.chat.id, mess[0][5],
    #                      reply_markup=lib.menu_ready(),
    #                      parse_mode='html')
    elif call.data == 'no':
        time_out = bot.send_message(call.message.chat.id, mess[99][6])
        sleep(5)
        bot.delete_message(call.message.chat.id, time_out.id)
        sleep(5)
        # bot.delete_message(call.message.chat.id, time_out.id)
        bot.send_message(call.message.chat.id,
                         mess[0][4],
                         reply_markup=kb.simple_menu())
    # 'Yes_HR','No_HR' реакция о вопросе про документы
    elif call.data == 'Yes_HR':
        chif = bot.edit_message_text(mess[1][5], call.message.chat.id, call.message.id)

        # sleep(18000)    # установка таймера на 5 часа после сообщения
        sleep(5)
        bot.delete_message(call.message.chat.id, chif.id)
        bot.send_message(call.message.chat.id, '====17:00====')

        bot.send_message(call.message.chat.id,
                         mess[1][6],
                         reply_markup=kb.simple_menu(call_yes='yes_answer', call_no='no_answer'),
                         disable_notification=True)
    elif call.data == 'No_HR':
        time_out = bot.send_message(call.message.chat.id, mess[99][6])
        sleep(5)
        bot.delete_message(call.message.chat.id, time_out.id - 1)
        bot.delete_message(call.message.chat.id, time_out.id)
        sleep(5)
        bot.send_message(call.message.chat.id,
                         f'{employee.name}, {mess[1][4]}',
                         reply_markup=kb.simple_menu('Yes_HR', 'No_HR'))
    # 'yes_answer', 'no_answer' реакция на приглашение к опросу
    elif call.data == 'yes_answer':
        if employee.name_questionnaire == QUEST_FIRST_LIST:
            id_mess = bot.edit_message_text(mess[99][8], call.message.chat.id, call.message.id)
            employee.survey_first_day(id_mess.id)
        elif employee.name_questionnaire == QUEST_SECOND_LIST:
            id_mess = bot.edit_message_text(mess[99][12], call.message.chat.id, call.message.id)
            employee.survey_first_day(id_mess.id, type_quest=2)
        elif employee.name_questionnaire == TEXT_QUESTIONNAIRES:
            # id_mess = bot.edit_message_text(mess[99][13], call.message.chat.id, call.message.id)
            bot.edit_message_text(mess[99][13], call.message.chat.id, call.message.id)

            employee.quest_rez[employee.adaptation_dey] = []
            send_next_question()

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
    elif call.data.isdigit() and (0 < int(call.data) < 11):  # Проверка callback если нажата числовая кнопка
        pass


@bot.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text.lower() == 'удалить' or message.text.lower() == 'elfkbnm':
        del_chat = employees.pop(message.chat.id, 'Такого чата в базе нет')
        bot.send_message(message.chat.id, del_chat, reply_markup=types.ReplyKeyboardRemove())


    # ========== Переделать с учетом изменения в словаре сообщений
    elif message.text[:6] == 'Прошел':  # Реакция на нажатие кнопки "Прошел"
        #    elif message.text == 'Прошел✔️':  # Реакция на нажатие кнопки "Прошел"

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
            # Окончание адаптации
            with open('./pic/Hand_.well_done.tgs', 'rb') as file:
                bot.send_sticker(message.chat.id,
                                 file,
                                 reply_markup=types.ReplyKeyboardRemove())

            bot.send_message(message.chat.id, mess[99][5])
            employees[message.chat.id].adaptation_completed = True
            lib.dump_employees(employees)

    elif message.text.lower() == 'adm_sys':  # создает файл с информацией о пользователе
        lib.sys_info(employees)
        try:
            with open(r'./employ_data.txt', 'rb') as file:
                bot.send_document(message.chat.id,
                                  file,
                                  caption='Файл создан')
        except FileNotFoundError:
            bot.send_message(message.chat.id, 'Документ не найден')
    else:
        bot.send_message(message.chat.id, mess[99][7])  # сообщение бота на любой ввод не учтенный в коде


if __name__ == '__main__':
    while True:  # Цикл для постоянного перезапуска бота
        try:
            print('Мой HR-бот')
            print(lib.format_time(time()))
            # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
            print('Started')
            bot.polling(none_stop=True, interval=0, skip_pending=True)
        except:
            logger.exception()
            continue
    print('Stoped')
