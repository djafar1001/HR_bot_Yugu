import telebot

# Замените 'TOKEN' на ваш токен API Telegram Bot
bot = telebot.TeleBot('TOKEN')

# Выборочные данные по имеющимся вакансиям и требованиям
vacancies = {
    'Инженер-программист': 'Требования: Python, Java, опыт веб-разработки',
    'Аналитик данных': 'Требования: SQL, визуализация данных, статистический анализ',
    'Специалист по маркетингу': 'Требования: маркетинг в социальных сетях, создание контента',
}

# Образец ссылки на веб-страницу компании с информационными документами
company_webpage = 'https://www.example.com/vacancies'

# Образцы контактных телефонов для отдела кадров
contact_phone_numbers = ['+1234567890', '+9876543210']

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Добро пожаловать в бот вакансий!')

@bot.message_handler(commands=['vacancies'])
def list_vacancies(message):
    # Получение и отправка списка имеющихся вакансий
    vacancies_list = '\n'.join(vacancies.keys())
    bot.reply_to(message, f'Имеющиеся вакансии:\n{vacancies_list}')

@bot.message_handler(commands=['requirements'])
def vacancy_requirements(message):
    # Проверьте, указана ли вакансия
    command_parts = message.text.split()
    if len(command_parts) > 1:
        vacancy = ' '.join(command_parts[1:])
        if vacancy in vacancies:
            requirements = vacancies[vacancy]
            bot.reply_to(message, f'Требования к {vacancy}:\n{requirements}')
        else:
            bot.reply_to(message, f'Вакансия "{vacancy}" не найдено.')
    else:
        bot.reply_to(message, 'Пожалуйста, укажите вакансию.')

@bot.message_handler(commands=['documents'])
def vacancy_documents(message):
    # Отправьте ссылку на веб-страницу компании с информационными документами
    bot.reply_to(message, f'Информационные документы по нашим вакансиям вы можете найти здесь:\n{company_webpage}')

@bot.message_handler(commands=['contact'])
def contact_hr(message):
    # Отправьте контактные телефоны отдела кадров
    contact_numbers = '\n'.join(contact_phone_numbers)
    bot.reply_to(message, f'Свяжитесь с нашим отделом кадров по адресу:\n{contact_numbers}')

bot.polling()