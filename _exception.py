@bot.message_handler(commands=['start'])
def handle_start(message, employee=None):
    # Запрос имени сотрудника
    answer = bot.send_message(message.chat.id, "Пожалуйста, укажите, как к Вам можно обращаться:")
    bot.register_next_step_handler(answer, start_dialog)


def start_dialog(message):
    bot.send_message(message.chat.id, f'{message.text} с началом трудовой деятельности')

    markup = types.InlineKeyboardMarkup(row_width=2)
    butt_yes = types.InlineKeyboardButton('Да', callback_data='1')
    butt_no = types.InlineKeyboardButton('Нет', callback_data='0')
    markup.add(butt_yes, butt_no)

    bot.send_message(message.chat.id,
                     f'{message.text} Вы готовы приступить к работе по адаптации?',
                     reply_markup=markup)

    @bot.callback_query_handlers(func=lambda call: True)
    def reaktion(call):
        if call.data == '1':
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text=f'{employee.name} сегодня в рамках программы адаптации\n'
                                       f'Вам необходимо пройти вводный курс\n'
                                       f'"Добро пожаловать yна предприятие" ')
        pass
