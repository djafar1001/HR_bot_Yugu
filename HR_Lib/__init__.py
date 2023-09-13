from datetime import datetime

from telebot import types
import pickle


def format_time(timestamp) -> str:
    """
    Функция перевода времени из Unix формата
    :param timestamp: int: дата в формате Unix
    :return: df_time: str: строка с преобразованным форматом данных
    """
    dt_object = datetime.fromtimestamp(timestamp)
    df_time = f'{dt_object:%d-%m-%Y %H:%M:%S}'

    return df_time


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


def menu_ready():
    """
    Функция организации Reply-меню для завершения этапа прохождения адаптации
    :return: kb:ReplyKeyboard
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton(text='Прошел✔️')
    kb.add(btn_1)

    return kb


def sys_info(employees):
    """
    Функция Записывает данные о пользователях бота в текстовый файл
    :param employees: dict - словарь с пользователями бота
    :return: file
    """
    with open('employ_data.txt', 'w', encoding='UTF-8') as file:
        file.write('id пользователя | информация о пользователе\n')
        for i_id, i_exploy in employees.items():
            file.write(f'  {i_id}     | {i_exploy}\n')


def time_begin():
    return datetime.now()


def dump_employees(employees):
    """Функция сохранения словаря пользователей в битный файл"""
    with open('./data/employees.db', 'wb') as file:  # !!!нужно создать функцию
        pickle.dump(employees, file)


# def user_verification(id_user, employees):
#     if id_user in employees.keys():
#
#     else:
#         return False
def day_score(employee):
    pass
