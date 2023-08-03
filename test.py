from setings_HR import HR_BOT_TOKEN as TOKEN
import telebot
from telebot import types
from time import sleep

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN['token'])

keyboard = types.ReplyKeyboardMarkup(row_width=2)
button1 = types.KeyboardButton('Button 1')
button2 = types.KeyboardButton('Button 2')  # Highlighted button
button3 = types.KeyboardButton('Button 3')
keyboard.add(button1, button2, button3)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Select an option:", reply_markup=keyboard)
    sleep(20)


bot.polling()
