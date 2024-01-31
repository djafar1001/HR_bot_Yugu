import telebot
# from class_user import Employee
from main_new import Employee
import Lib.keyboard as kb
from setings_HR_new import BOT_MESSAGE as mess

def check_work(employee: Employee, bot: telebot.TeleBot):
    if not employee.adaptation_completed:
        not_completed = employee.courses.index(0)
        bot.send_message(employee.id_user,
                         mess[99][4],
                         disable_notification=True,
                         reply_markup=kb.simple_menu())



