"""
Параметры для HR бота
"""

HR_BOT_TOKEN = {'name': '@Yugu_HR_bot',
                'URL': 'https://t.me/Yugu_HR_bot',
                'token': '6096922509:AAEVP8m7xiSLll0nZH7Z257siv4wasPxGEw'}

# Сообщение для команды /help
HELP_MESS = 'Курсы находятся на корпоративном портале,' \
            '\nв разделе "Карьера и развитие" выбираем "Учебный портал".' \
            '\n на странице портала выбираем "Дистанционное обучение"' \
            '\nи в поисковой строке указываем нужный курс'

"""
Словарь сообщений которые выдает бот в соответствии ключами.
Ключи: 99 - служебные сообщения, 
        0 - сообщения приветствия за день до начала работы, 
        1 - сообщения 1-го дня, 
        2 - сообщения 2-го дня
"""
BOT_MESSAGE = {
    99:{
        1: 'Здравствуйте!\nЯ ассистент который поможет Вам адаптироваться на новом рабочем месте',
        2: "Пожалуйста, укажите, как к Вам можно обращаться:",
        3: '\nАдаптация начнется завтра.'
           '\nДля эффективной работы проверьте  включены ли уведомления',
        4: 'До завтра',
        5: 'Есть ли у Вас доступ к компьютер на рабочем месте?',
        6: 'Вы готовы приступить к работе по адаптации?',
        7: 'После того, как пройдёте этот курс, нажмите кнопку <b>«Прошел»</b> внизу чата 👇',
        8: 'Вы готовы продолжать адаптацию',
        9: 'Вы успешно прошли все этапы адаптации'
           '\nУдачи в работе',
        10: 'Хорошо я вам напомню через час',
        11: 'Я настроен для начальной адаптации новых сотрудников'
            '\nК сожалению, я не могу Вам помочь в этом вопросе.😞'
    },
    0: {
        1: "Доброе утро!"
           "\nC первым рабочим днем в Банке России",
        2: 'Для адаптации я буду Вам последовательно'
           '\nрекомендовать курсы для прохождения.'
           '\nИнформация о расположении курсов по команде /help',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
        8: '',
        9: '',
        10: ''
    },

    1: {
        1: 'C началом трудовой деятельности в Банке России',
        2: 'сегодня в рамках программы адаптации'
           '\nВам необходимо пройти вводный курс'
           '\n<b>"Добро пожаловать в Банк России"</b>',
        3: 'Вам необходимо пройти дистанционный курс\n'
           '<b>«Основы антикоррупции»</b>',
        4: 'Далее необходимо пройти дистанционный курс'
           '\n<b>«Обеспечение информационной безопасности при обработке '
           'информации ограниченного доступа в Банке России»</b>'
           '\nи тестирование по нему',
    },
    2: {
        4: 'Сегодня в рамках программы адаптации тебе необходимо пройти'
           '\nдистанционный курс <b>«Общение без ограничений»</b>',
        5: 'Осталось пройти, в рамках адаптации, последний но не менее важный курс'
           '\n<b>«Дистанционный курс и тестирование по САДД БР»</b>'
           '\nи обязательно выполнить тестирование по нему '
    }
}