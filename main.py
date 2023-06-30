"""
HRБот– виртуальный ассистент предназначенный для коммуникации
с принятыми в Банк России на работу сотрудниками,
обученный общаться по ограниченному кругу сценариев
Бот обрабатывает командыЖ
start - запуск бота
edit - редактирует имя
continue - продолжение работы с ботом
help - информация о нахождении курсов

"""
from setings_HR import HR_BOT_TOKEN as TOKEN, BOT_MESSSAGE as mess, HELP_MESS
import HR_Lib as lib

import telebot
from telebot import types
from os import path, remove

import pickle
from time import time, sleep

# Создание экземпляра бота с использованием токена
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду


# Класс, представляющий нового сотрудника
class Employee:
    def __init__(self, name):
        self.name = name
        #        self.training_start = datetime.now()
        self.training_start = time()
        self.adaptation_dey = 1
        self.current_course = 1
        self.courses_completed = [0] * 5

    def __str__(self):
        return f'Пользователь {self.name} начал адаптацию {lib.format_time(self.training_start)}\n' \
               f'сейчас изучает курс {self.current_course} всего изучено {str(self.courses_completed)}'


# Открываем или создаем словарь для хранения данных о сотрудниках
if path.exists('employees.db'):
    with open('employees.db', 'rb') as file:
        employees = pickle.load(file)
else:
    employees = {}


@bot.message_handler(commands=['start'])
def handle_start(message, employee=None):
    """
    После ввода команды /start Проверяем наличие пользователя в словаре сотрудников
    и в случае отсутствия запрашиваем его имя. Полученный результат передаем
    в функцию start_dialog

    :param message:
    :return:
    """
    if message.chat.id not in employees.keys():
        bot.send_message(message.chat.id, mess[0][1])
        with open('./pic/AnimatedSticker_hi.tgs', 'rb') as file:
            bot.send_sticker(message.chat.id, file)
        # Запрос имени сотрудника
        answer = bot.send_message(message.chat.id, mess[0][2])
        bot.register_next_step_handler(answer, start_dialog)
    else:
        employee = employees[message.chat.id]
        #       print(employee.__str__())
        bot.send_message(message.chat.id, employee.__str__())
        #       bot.send_message(message.chat.id, str(employee.courses_completed))

        if not all(employees[message.chat.id].courses_completed):
            bot.send_message(message.chat.id, 'Давайте продолжим')
        else:
            bot.send_message(message.chat.id, 'Вы успешно прошли все этапы адаптации'
                                              '\nУдачи в работе')


def start_dialog(message):
    """
    Создание объекта сотрудника и сохранение его в словаре по
    идентификатору чата с последующей сериализацией в битовый файл/
    Выполняем диалог первого дня

    :param message:
    :return:
    """
    employee = Employee(message.text)
    employees[message.chat.id] = employee

    with open('employees.db', 'wb') as file:  # !!!нужно создать функцию
        pickle.dump(employees, file)

    bot.send_message(message.chat.id, f'Рад знакомству <b>{employee.name}</b>!\n{mess[0][3]}!', parse_mode='html')
    #    bot.send_message(message.chat.id, f'{employee.name} с началом трудовой деятельности в Банке Росси')

    # markup = types.InlineKeyboardMarkup(row_width=2)
    # butt_yes = types.InlineKeyboardButton('Да', callback_data='1')
    # butt_no = types.InlineKeyboardButton('Нет', callback_data='0')
    # markup.add(butt_yes, butt_no)

    # bot.send_message(message.chat.id,
    #                  f'{employee.name} Вы готовы приступить к работе по адаптации?',
    #                  reply_markup=lib.simple_menu())
    bot.send_message(message.chat.id,
                     mess[0][4],
                     reply_markup=lib.simple_menu())

    @bot.callback_query_handler(func=lambda call: True)
    def pressing_reaction(call):
        if call.data == '1':
            if employee.current_course > 3:
                employee.adaptation_dey = 2
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text=f'<b>{employee.name}</b> {mess[employee.adaptation_dey][employee.current_course]}',
                                  parse_mode='html')
            bot.send_message(call.message.chat.id, mess[0][5],
                             reply_markup=lib.menu_ready(),
                             parse_mode='html')
        else:
            ...


@bot.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text.lower() == 'удалить' or message.text.lower() == 'elfkbnm':
        path_file = 'employees.db'
        try:
            remove(path_file)
        except:
            bot.send_message(message.chat.id, f'Файл {path_file} не найден')
    #       employees = {}
    elif message.text == 'Прошел✔️':

        employees[message.chat.id].courses_completed[employees[message.chat.id].current_course - 1] = 1
        employees[message.chat.id].current_course += 1

        bot.send_message(message.chat.id, mess[0][6],
                         reply_markup=lib.simple_menu())


if __name__ == '__main__':
    print('Мой HR-бот')
    print(lib.format_time(time()))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)

    print('Stoped')
