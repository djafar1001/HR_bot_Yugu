import telebot
import datetime
import pickle

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# Класс пользователя
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.responses = {}  # Словарь для хранения ответов пользователя

    def add_response(self, question_number, response):
        self.responses[question_number] = response

    def get_responses(self):
        return self.responses

# Словарь пользователей
users = {}

# Функция для отправки опроса пользователю
def send_survey(user_id, question_list):
    for i, question in enumerate(question_list, start=1):
        bot.send_message(user_id, f"Вопрос {i}:\n{question}")

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

# Отправка опросов
def send_daily_survey():
    today = datetime.date.today()
    day_number = today.day

    if day_number in questions:
        question_list = questions[day_number]
        for user_id, user in users.items():
            if user_id not in user.get_responses():  # Проверка, что пользователь еще не отвечал на вопросы
                send_survey(user_id, question_list)

# Инициализация пользователей (вызывать при старте бота)
def initialize_users():
    global users
    users = load_survey_results()  # Загрузка данных о пользователях и ответах из файла (если есть)

# Обработчик команды /start (вызывать при старте бота)
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = User(user_id)
        save_survey_results()  # Сохранение данных о новом пользователе
    send_daily_survey()  # Отправка опроса при старте бота

# Обработчик текстовых сообщений (ввод ответов на вопросы)
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_id = message.from_user.id
    if user_id in users:
        user = users[user_id]
        responses = user.get_responses()
        if user_id not in responses:
            question_number = datetime.date.today().day
            response = message.text
            user.add_response(question_number, response)
            save_survey_results()  # Сохранение ответа
            bot.send_message(user_id, "Спасибо за ответ!")
            send_daily_survey()  # Отправка следующего вопроса (если есть)

# Инициализация и запуск бота
if __name__ == "__main__":
    initialize_users()  # Инициализация пользователей
    bot.polling(none_stop=True)
