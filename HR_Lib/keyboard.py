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