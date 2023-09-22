from setings_test import TOKEN_T_BOT as TOKEN
import HR_Lib as lib
import telebot
import datetime
import pickle
from time import time
bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду


# Класс пользователя
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.responses = {}
        self.registration_date = datetime.date.today()  # Дата регистрации пользователя

    def add_response(self, question_number, response):
        self.responses[question_number] = response

    def get_responses(self):
        return self.responses

    def get_day_number(self):
        today = datetime.date.today()
        delta = today - self.registration_date
        return delta.days

    def change_day_number(self, new_day_number):
        # Изменение номера дня (для тестирования)
        self.registration_date = datetime.date.today() - datetime.timedelta(days=new_day_number - 1)

# Словарь пользователей
users = {}

# Функция для отправки следующего вопроса
def send_next_question(user_id):
    user = users[user_id]
    day_number = user.get_day_number()

    if day_number in questions:
        question_list = questions[day_number]
        for i, question in enumerate(question_list):
            if i not in user.get_responses():
                bot.send_message(user_id, f"Вопрос {i + 1}:\n{question}")
                return True  # Вопрос отправлен
    return False  # Вопросы закончились

# Функция для сохранения результатов опросов
def save_survey_results():
    with open("user_responses.pkl", "wb") as file:
        pickle.dump(users, file)

# Функция для загрузки результатов опросов (если есть)
def load_survey_results():
    try:
        with open("user_responses.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

# Обработчик команды /start (вызывать при старте бота)
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = User(user_id)
        save_survey_results()  # Сохранение данных о новом пользователе
    send_next_question(user_id)  # Отправка первого вопроса при старте бота

# Обработчик текстовых сообщений (ввод ответов на вопросы)
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_id = message.from_user.id
    if user_id in users:
        user = users[user_id]
        responses = user.get_responses()
        if send_next_question(user_id):
            # Если есть следующий вопрос, ожидаем ответ пользователя
            question_number = user.get_day_number()
            response = message.text
            user.add_response(question_number, response)
            save_survey_results()  # Сохранение ответа
        else:
            bot.send_message(user_id, "Спасибо за ответы на все вопросы!")

# Создание инлайн-клавиатуры 2x5 для оценки
def create_inline_keyboard_2x5():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for i in range(1, 11):
        button = telebot.types.InlineKeyboardButton(str(i), callback_data=f"rating_{i}")
        markup.add(button)
    return markup

# Обработчик для инлайн-клавиш оценки
@bot.callback_query_handler(lambda call: call.data.startswith('rating_'))
def handle_rating_callback(call):
    user_id = call.from_user.id
    rating = int(call.data.split('_')[1])
    user = users.get(user_id)
    if user:
        question_number = user.get_day_number()
        user.add_response(question_number, rating)
        save_survey_results()  # Сохранение ответа
        if not send_next_question(user_id):
            bot.send_message(user_id, "Спасибо за ответы на все вопросы!")

# Определение вопросов для каждого дня, недели и квартала
questions = {
    1: ["Сообщи о возможных идеях улучшения качества работы чат бота?",
        "Сообщи о возможных идеях улучшения работы по адаптации новых сотрудников"],
    2: ["Что можно было бы организовать по-другому в работе чат бота?",
        "С какими проблемами ты встретился по адаптации?"],
    5: ["Что понравилось?",
        "Что не понравилось?",
        "Как часто за эту неделю ты общался со своим руководителем?",
        "Как часто за эту неделю ты общался с ответственным за адаптацию?",
        "Получил ли ты ответы на все свои вопросы?"],
}

# Инициализация и запуск бота
if __name__ == "__main__":
    users = load_survey_results()  # Загрузка результатов опросов
    print('Мой HR-бот')
    print(lib.format_time(time()))
    # Запуск бота в работу на ожидание сообщений в бесконечном режиме без интервалов
    print('Started')
    bot.polling(none_stop=True, interval=0)
    print('Stoped')
