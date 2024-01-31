from setings_HR_new import HR_BOT_TOKEN as TOKEN, \
    BOT_MESSAGE as mess, \
    HELP_MESSAGE, QUEST_FIRST_LIST, QUEST_SECOND_LIST, ADM_MESS
from setings_test import TOKEN_T_BOT as TOKEN
import Lib as lib
import telebot
import datetime
import pickle
from time import time, sleep
from os import path



bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду


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

    def survey_first_day(self, id_mess, type_quest=1):
        """
        Функция опросника в первый рабочий день. Данные заносятся в self.score_dey
        да - 1, нет - 0 вопросы берутся из словаря questions файла setings_HR_new
        :return: None
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
            bot.delete_message(self.id_user, self.id_hi)
            #notification_9_00(employees, self.id_user)

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
                                       f'id чата:{self.id_user}\n')


# Открываем или создаем словарь для хранения данных о сотрудниках
if path.exists('Employee/employees.db'):
    with open('Employee/employees.db', 'rb') as file:
        employees = pickle.load(file)
else:
    employees = {}

# Вопросы опросников кроме последнего
questions = {
    3: [
        "Сообщи о возможных идеях улучшения качества работы чат бота?",
        "Сообщи о возможных идеях улучшения работы по адаптации новых сотрудников",
        "Оцени собственный прогресс в достижении цели «Получение знаний об организации» (от 1 до 10)",
    ],
    4: [
        "Что можно было бы организовать по-другому в работе чат бота?",
        "С какими проблемами ты встретился по адаптации?",
        "Оцени собственный прогресс в достижении цели «Получение знаний об организации» (от 1 до 10)",
    ],
    5: ["Что понравилось?",
        "Что не понравилось?",
        "Как часто за эту неделю ты общался со своим руководителем?",
        "Как часто за эту неделю ты общался с ответственным за адаптацию?",
        "Получил ли ты ответы на все свои вопросы?"
        ]
}


# Функция для загрузки результатов опросов (если есть)
def load_survey_results():
    try:
        with open("user_responses.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}


# Инициализация пользователей (вызывать при старте бота)
def initialize_users():
    global users
    users = load_survey_results()  # Загрузка данных о пользователях и ответах из файла (если есть)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in employees:
        employees[user_id] = User(user_id)
        save_survey_results()  # Сохранение данных о новом пользователе
    send_next_question(user_id)  # Отправка первого вопроса при старте бота


# ================================================================
# Обработчик команды /changeday (для отладки)
@bot.message_handler(commands=['changeday'])
def change_day_command(message):
    user_id = message.from_user.id
    if user_id in users:
        user = users[user_id]
        user.change_day_number(2)  # Здесь можно установить номер дня для тестирования
        bot.send_message(user_id, f"Номер дня изменен на {user.get_day_number()}")
