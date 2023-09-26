from setings_test import TOKEN_T_BOT as TOKEN
import HR_Lib as lib
import telebot
from telebot import types
# import datetime
# import pickle
from time import time

bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду

global user


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
        self.name_questionnaire = questions_dict
        self.second_quest = False
        self.check_score = 0  # Значение оценки для опросника (1-да, 0-нет)
        self.adaptation_completed = False  # параметр окончания адаптации
        self.index_question = 0  # Индекс вопросов в списке опросника
        self.lost_message = None
        self.id_hi = 0  # индекс стикера приветствия
        self.survey_days = [3, 4, 5]


quest_rez = {}

questions_dict = {
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
    5: [
        "Что понравилось?",
        "Что не понравилось?",
        "Как часто за эту неделю ты общался со своим руководителем?",
        "Как часто за эту неделю ты общался с ответственным за адаптацию?",
        "Получил ли ты ответы на все свои вопросы?"
    ]
}


def send_next_question():
    """
    Функция направляет очередной вопрос из списка по ключу равному номеру дня адаптации
    """
    if user.index_question < len(questions_dict[user.adaptation_dey]):
        query = bot.send_message(user.id_user, f'Вопрос {user.index_question + 1}\n'
                                               f'{questions_dict[user.adaptation_dey][user.index_question]}')
        bot.register_next_step_handler(query, save_query)
    else:
        bot.send_message(user.id_user, 'Спасибо за пройденный опрос')
        user.index_question = 0
        # ===========================
        if user.survey_days:
            continue_quest()
        else:
            bot.send_message(user.id_user, f'quest_rez={quest_rez}')
            bot.send_message(user.id_user, 'Тестирование закончено')


def continue_quest():
    """ВРЕМЕННАЯ Функция изменение номера дня адаптации"""
    user.adaptation_dey = user.survey_days.pop(0)
    quest_rez[user.adaptation_dey] = []
    bot.send_message(user.id_user, f'День {user.adaptation_dey}, осталось {user.survey_days}')
    send_next_question()


# ===========================
def save_query(message):
    """
    Функция сохраняет ответ пользователя в список ответов,
    привязанный к ключу дня адаптации, в соответствии с индексом вопросов
    И выполняет запуск функции вывода очередного вопроса
    """
    quest_rez[user.adaptation_dey].append(message.text)
    user.index_question += 1
    send_next_question()


# ==================================================
def simple_menu(call_yes='yes', call_no='no'):
    """
    Функция определения Inline-меню с двумя кнопками "Да" и "Нет"
    :return: markup: InlineKeyboard
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    butt_yes = types.InlineKeyboardButton('Да', callback_data=call_yes)
    butt_no = types.InlineKeyboardButton('Нет', callback_data=call_no)
    markup.add(butt_yes, butt_no)

    return markup


# ===================================================


@bot.message_handler(commands=['start'])
def handle_start(message):
    """Функция обработки команды start"""
    # Создание экземпляра пользователя
    global user
    user = Employee('Alex', message.chat.id)
    # user.adaptation_dey = choice_day()
    user.adaptation_dey = user.survey_days.pop(0)
    bot.send_message(user.id_user, f'День {user.adaptation_dey}, осталось {user.survey_days}')
    bot.send_message(user.id_user, 'Вы готовы пройти опрос?', reply_markup=simple_menu('yes', 'no'))
    pass


@bot.message_handler(commands=['changeday'])
def change_day_command(message):
    """Функция обработки команды changeday"""
    pass


# @bot.message_handler(content_types=['text'])
# def text_reaction(message):
#     if user.question_process:
#         pass


@bot.callback_query_handler(func=lambda call: True)
def pressing_reaction(call):
    if call.data == 'yes':
        quest_rez[user.adaptation_dey] = []
        send_next_question()
    elif call.data == 'no':
        bot.send_message(user.id_user, 'Жаль, нам очень важно Ваше мнение')


# Инициализация и запуск бота
if __name__ == "__main__":
    print('Мой HR-бот')
    print(lib.format_time(time()))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)
    print('Stopped')
