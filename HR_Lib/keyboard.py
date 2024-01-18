from telebot import types


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


def create_inline_keyboard_2x5():
    """
    Функция создает inline-меню из 10 кнопок в 2 ряда по 5 в каждом
    с соответствущим числом и callbeck = этому числу в str
    """
    markup = types.InlineKeyboardMarkup()

    row1 = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 6)]
    row2 = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(6, 11)]

    markup.row(*row1)  # Первый ряд
    markup.row(*row2)  # Второй ряд

    return markup