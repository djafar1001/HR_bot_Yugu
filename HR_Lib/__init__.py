from datetime import datetime
from telebot import types


def format_time(timestamp) -> str:
    """
    Функция перевода времени из Unix формата
    :param timestamp: int: дата в формате Unix
    :return: df_time: str: строка с преобразованным форматом данных
    """
    dt_object = datetime.fromtimestamp(timestamp)
    df_time = f'{dt_object:%d-%m-%Y %H:%M:%S}'

    return df_time


def simple_menu():
    """
    Функция определения Inline-меню с двумя кнопками "Да" и "Нет"
    :return: markup: InlineKeyboard
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    butt_yes = types.InlineKeyboardButton('Да', callback_data='1')
    butt_no = types.InlineKeyboardButton('Нет', callback_data='0')
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
            file.write(f'  {i_id}     | {i_exploy}\n' )
