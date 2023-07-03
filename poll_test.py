from setings_HR import HR_BOT_TOKEN as TOKEN
import telebot
from telebot import types
import json

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN['token'])

# Создание словаря для хранения результатов опроса
poll_results = {}

# Вопросы опроса
questions = [
    'Вам было удобно работать с чат ботом?',
    'Материалы адаптации были понятны и доступны',
    'Оцените собственный прогресс в достижении цели «Получение знаний о Предприятии»',
    'Пожелания в работе бота:'
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправка первого вопроса опроса пользователю
    send_question(message.chat.id, 0)

# Функция для отправки вопроса пользователю
def send_question(chat_id, question_index):
    if question_index >= len(questions):
        # Все вопросы опроса заданы, завершение опроса
        finish_poll(chat_id)
        return

    question = questions[question_index]
    if question_index == len(questions) - 1:
        # Последний вопрос - пожелания в работе бота
        bot.send_message(chat_id=chat_id, text=question, disable_web_page_preview=True)
    else:
        # Остальные вопросы - выбор варианта ответа
        options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        poll = types.Poll(question=question, options=options, is_anonymous=False)
        sent_poll = bot.send_poll(chat_id=chat_id, question=poll.question, options=poll.options, is_anonymous=poll.is_anonymous)
        poll_results[sent_poll.poll.id] = {}  # Добавляем идентификатор опроса в словарь результатов

# Обработчик ответов на опрос
@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    poll_id = poll_answer.poll_id
    user_id = poll_answer.user.id
    selected_option = poll_answer.option_ids[0]  # Пользователь может выбрать несколько вариантов, берем первый
    poll_results[poll_id][user_id] = selected_option

    # Переход к следующему вопросу
    question_index = len(poll_results[poll_id])
    send_question(poll_answer.user.id, question_index)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    if message.text == 'Пожелания в работе бота:':
        # Запрашиваем ввод рекомендаций
        bot.send_message(chat_id=message.chat.id, text='Введите ваши рекомендации:')
        bot.register_next_step_handler(message, save_recommendations)
    else:
        # Отправка следующего вопроса
        question_index = len(poll_results)  # Используем длину словаря результатов в качестве индекса вопроса
        send_question(message.chat.id, question_index)

# Функция для сохранения рекомендаций
def save_recommendations(message):
    poll_results['Рекомендации'] = message.text
    finish_poll(message.chat.id)

# Функция для завершения опроса и сохранения результатов в файл
def finish_poll(chat_id):
    # Записываем результаты опроса в файл
    with open('poll_results.json', 'w') as file:
        json.dump(poll_results, file)

    bot.send_message(chat_id=chat_id, text='Опрос завершен. Результаты сохранены.')

# Запуск бота
bot.polling()
