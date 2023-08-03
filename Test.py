from setings_HR import HR_BOT_TOKEN as TOKEN, BOT_MESSAGE as mess, HELP_MESS
#import HR_Lib as lib

import telebot
#from telebot import types
from time import time, sleep
bot = telebot.TeleBot(TOKEN['token'])  # привязка бота к коду

# Отправка push-уведомления пользователю
def send_notification(chat_id, message):
    # Используйте метод sendMessage с параметром disable_notification=True
    sleep(10)
    bot.send_message(chat_id, message, disable_notification=True)

# Команда для отправки уведомления
@bot.message_handler(commands=['send_notification'])
def send_custom_notification(message):
    # Проверка, что уведомления включены для пользователя
    if is_notifications_enabled(message.chat.id):
        # Отправка push-уведомления пользователю
        send_notification(message.chat.id, 'Пора выполнить работу с ботом!')
    else:
        bot.send_message(message.chat.id, 'Не удалось направить уведомления')

# Проверка, включены ли уведомления для пользователя
def is_notifications_enabled(chat_id):
    # Здесь вы можете использовать базу данных или другой механизм для хранения состояния пользователя
    # и проверить, установлен ли флаг "Уведомления включено" для данного chat_id
    # Верните True, если уведомления включены, и False в противном случае
    return True

# Запуск бота
bot.polling()
