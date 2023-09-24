from setings_test import TOKEN_T_BOT as TOKEN
import HR_Lib as lib
import telebot
import datetime
import pickle
from time import time
bot = telebot.TeleBot(TOKEN.get('token'))  # привязка бота к коду


# Класс пользователя
class User:
    def __init__(self, user_id, registration_date):
        self.user_id = user_id
        self.registration_date = registration_date
        self.responses = {}  # Словарь для хранения ответов пользователя на вопросы

    def add_response(self, day_number, response):
        if day_number not in self.responses:
            self.responses[day_number] = []
        self.responses[day_number].append(response)

    def get_responses(self):
        return self.responses

    # Функция для перехода к следующему вопросу
    def next_question(self):
        self.day_number += 1  # Увеличиваем номер дня
        self.responses[self.day_number] = {}  # Создаем словарь для ответов на новый день



    def get_day_number(self):
        today = datetime.date.today()
        delta = today - self.registration_date
        return delta.days if delta.days >= 2 else 1

    def get_question_for_day(self, day_number):
        questions = [
            [
                "Сообщи о возможных идеях улучшения качества работы чат бота?",
                "Сообщи о возможных идеях улучшения работы по адаптации новых сотрудников",
                "Оцени собственный прогресс в достижении цели «Получение знаний об организации» (от 1 до 10)",
            ],
            [
                "Что можно было бы организовать по-другому в работе чат бота?",
                "С какими проблемами ты встретился по адаптации?",
                "Оцени собственный прогресс в достижении цели «Получение знаний об организации» (от 1 до 10)",
            ],
            [
                "Что понравилось?",
                "Что не понравилось?",
                "Как часто за эту неделю ты общался со своим руководителем?",
                "Как часто за эту неделю ты общался с ответственным за адаптацию?",
                "Получил ли ты ответы на все свои вопросы?",
            ],
        ]
        if day_number <= len(questions):
            return questions[day_number - 1]
        else:
            return []

    def change_day_number(self, new_day_number):
        # Изменение номера дня (для тестирования)
        self.registration_date = datetime.date.today() - datetime.timedelta(days=new_day_number - 1)

#==================================





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
#================================================================
# Обработчик команды /changeday (для отладки)
@bot.message_handler(commands=['changeday'])
def change_day_command(message):
    user_id = message.from_user.id
    if user_id in users:
        user = users[user_id]
        user.change_day_number(2)  # Здесь можно установить номер дня для тестирования
        bot.send_message(user_id, f"Номер дня изменен на {user.get_day_number()}")
#==================================================================

# Обработчик текстовых сообщений (ввод ответов на вопросы)
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_id = message.from_user.id
    if user_id in users:
        user = users[user_id]
        day_number = user.get_day_number()
        questions = user.get_question_for_day(day_number)

        if questions:
            if send_next_question(user_id):
                # Если есть следующий вопрос, ожидаем ответ пользователя
                question_number = len(user.get_responses().get(day_number, [])) + 1
                response = message.text
                user.add_response(day_number, response)

                # Проверяем, есть ли еще вопросы
                if question_number < len(questions):
                    next_question = questions[question_number]
                    bot.send_message(user_id, next_question)
                else:
                    bot.send_message(user_id, "Спасибо за ответы на все вопросы!")
            else:
                bot.send_message(user_id, "Спасибо за ответы на все вопросы!")

# Создание инлайн-клавиатуры 2x5 для оценки
def create_inline_keyboard_2x5():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for i in range(1, 11):
        button = telebot.types.InlineKeyboardButton(str(i), callback_data=f"rating_{i}")
        markup.add(button)
    return markup


# Вспомогательная функция для отправки следующего вопроса
def send_next_question(user_id):
    user = users[user_id]
    day_number = user.get_day_number()
    questions = user.get_question_for_day(day_number)

    if questions:
        question_number = len(user.get_responses().get(day_number, [])) + 1
        if question_number <= len(questions):
            bot.send_message(user_id, questions[question_number - 1])
            return True
    return False

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



#=======================================================================

