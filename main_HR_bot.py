from setings_HR import HR_BOT_TOKEN as TOKEN
import telebot
from telebot import types
from datetime import datetime

#import markup_key as menu


# Создание экземпляра бота с использованием токена
# bot = telebot.TeleBot(HR_BOT_TOKEN.get('token'))  # привязка бота к коду
bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду


def format_time(timestamp: int) -> str:
    """
    Функция перевода времени из Unix формата
    :param timestamp: int: дата в формате Unix
    :return: df_time: str: строка с преобразованным форматом данных
    """
    dt_object = datetime.fromtimestamp(timestamp)
    df_time = f'{dt_object:%d-%m-%Y %H:%M:%S}'

    return df_time


# Класс, представляющий нового сотрудника
class Employee:
    def __init__(self, name):
        self.name = name
        self.courses_completed = 0


# Словарь для хранения данных о сотрудниках
employees = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создание объекта сотрудника и сохранение его в словаре по идентификатору чата
    employee = Employee(message.chat.id)
    employees[message.chat.id] = employee

    # Отправка приветственного сообщения
    bot.reply_to(message, f"Привет, {employee.name}! Добро пожаловать на предприятие!")

    # Запрос имени сотрудника
    bot.send_message(message.chat.id, "Пожалуйста, укажите, как к вам можно обращаться:")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    if chat_id in employees:
        employee = employees[chat_id]

        if not employee.name:
            # Сохранение имени сотрудника
            employee.name = message.text

            # Отправка сообщения с поздравлением и ссылкой на документ
            bot.send_message(chat_id, f"Поздравляю с первым рабочим днем, {employee.name}!")
            bot.send_message(chat_id, "C началом трудовой деятельности в предприятии! "
                                      "Ознакомьтесь с документом по ссылке: <ссылка>")

            # Запрос на ввод курсов
            bot.send_message(chat_id, "Для эффективной работы рекомендуется пройти следующие вводные курсы:")
            bot.send_message(chat_id, "1. Курс 1: <ссылка>")
            bot.send_message(chat_id, "2. Курс 2: <ссылка>")
            # ...

        elif employee.courses_completed < 2:
            # Обработка завершения курса
            employee.courses_completed += 1

            # Отправка нового задания
            bot.send_message(chat_id, "Поздравляю с успешным завершением курса! "
                                      "Теперь приступите к следующему заданию.")

            # Отправка ссылки на следующий курс
            bot.send_message(chat_id, f"Курс {employee.courses_completed + 1}: <ссылка>")

        else:
            # Запрос обратной связи
            bot.send_message(chat_id, "Пожалуйста, оцените свой опыт работы на предприятии "
                                      "и оставьте свои комментарии и предложения.")

    else:
        # Обработка случая, когда сотрудник не зарегистрирован
        bot.send_message(chat_id, "Пожалуйста, начните с команды /start для регистрации на предприятии.")

# Функция для отправки следующего вопроса
def send_question(chat_id, question_number):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 5

    for i in range(1, 11):
        button = types.InlineKeyboardButton(text=str(i), callback_data=f"question_{question_number}_{i}")
        markup.add(button)

    if question_number == 2:
        question = "2. Материалы по работе в предприятии были понятными и доступными?"
    elif question_number == 3:
        question = "3. Оцените ваш прогресс в достижении цели 'Изучение предприятия' (от 0 до 10):"

    bot.send_message(chat_id, question, reply_markup=markup)
# Запуск бота
bot.polling()
