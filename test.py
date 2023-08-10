TOKEN_T_BOT = {'name': '@Lear_telebot',
               'URL': 'https://t.me/Lear_telebot',
               'token': '5648782056:AAFw_vHn2dtZ5gvS_vOaz-_t2UnXVpimzgk'}
#from setings_HR import HR_BOT_TOKEN as TOKEN
import telebot
import schedule
import time
#from telebot import types
#from time import sleep

# Создание экземпляра бота
bot = telebot.TeleBot('5648782056:AAFw_vHn2dtZ5gvS_vOaz-_t2UnXVpimzgk')

# Словарь для хранения пользователей и их задач
users = {}

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.task_scheduled = False

    def schedule_task(self):
        if not self.task_scheduled:
            # Планируем задачу для пользователя
            schedule.every().day.at("09:00").do(self.send_task_notification)
            self.task_scheduled = True

    def send_task_notification(self):
        bot.send_message(self.user_id, "Задача для вас!")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id

    if user_id not in users:
        users[user_id] = User(user_id)
        bot.send_message(user_id, "Вы добавлены в систему. Задача будет запланирована для вас.")

    # Планирование задачи для пользователя
    users[user_id].schedule_task()

bot.polling()
