from datetime import datetime
from telebot import types
import pickle
# import keyboard, class_user
# requirements.txtrequirements.txtfrom .class_user import Employee

def format_time(timestamp) -> str:
    """
    Функция перевода времени из Unix формата
    :param timestamp: int: дата в формате Unix
    :return: df_time: str: строка с преобразованным форматом данных
    """
    dt_object = datetime.fromtimestamp(timestamp)
    df_time = f'{dt_object:%d-%m-%Y %H:%M:%S}'

    return df_time.replace(' ', '_')

#  ============= Перенесено в keyboard.py =======================
# def simple_menu(call_yes='yes', call_no='no'):
#     """
#     Функция определения Inline-меню с двумя кнопками "Да" и "Нет"
#     :return: markup: InlineKeyboard
#     """
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     butt_yes = types.InlineKeyboardButton('Да', callback_data=call_yes)
#     butt_no = types.InlineKeyboardButton('Нет', callback_data=call_no)
#     markup.add(butt_yes, butt_no)
#
#     return markup
#
#
# def menu_ready():
#     """
#     Функция организации Reply-меню для завершения этапа прохождения адаптации
#     :return: kb:ReplyKeyboard
#     """
#     kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_1 = types.KeyboardButton(text='Прошел✔️')
#     kb.add(btn_1)
#
#     return kb
#  ============================================================================

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
    with open('./Employee/employees.pkl', 'wb') as file:  # !!!нужно создать функцию
        pickle.dump(employees, file)

# def create_inline_keyboard_2x5():
#     """
#     Функция создает inline-меню из 10 кнопок в 2 ряда по 5 в каждом
#     с соответствущим числом и callbeck = этому числу в str
#     """
#     markup = types.InlineKeyboardMarkup()
#
#     row1 = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 6)]
#     row2 = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(6, 11)]
#
#     markup.row(*row1)  # Первый ряд
#     markup.row(*row2)  # Второй ряд
#
#     return markup


# def user_verification(id_user, employees):
#     if id_user in employees.keys():
#
#     else:
#         return False
def day_score(employee):
    pass
