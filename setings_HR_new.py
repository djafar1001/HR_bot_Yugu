"""
Параметры для HR бота
"""

HR_BOT_TOKEN = {'name': '@Yugu_HR_bot',
                'URL': 'https://t.me/Yugu_HR_bot',
                'token': '6096922509:AAEVP8m7xiSLll0nZH7Z257siv4wasPxGEw'}

# Сообщение для команды /help
HELP_MESSAGE = 'Курсы находятся на корпоративном портале,' \
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
        1: 'Есть ли у Вас доступ к компьютер на рабочем месте?',
        2: 'Вы готовы приступить к работе по адаптации?',
        3: 'После того, как пройдёте этот курс, нажмите кнопку <b>«Прошел»</b> внизу чата 👇',
        4: 'Вы готовы продолжать адаптацию',
        5: 'Вы успешно прошли все этапы адаптации'
           '\nУдачи в работе',
        6: 'Хорошо я вам напомню через час',
        7: 'Я настроен для начальной адаптации новых сотрудников'
           '\nК сожалению, я не могу Вам помочь в этом вопросе.😞',
        8: 'Выберите "да"  или "нет" в ответ на следующие вопросы',
        9: 'Спасибо.\nПоздравляю Вас с первым рабочим днем!'
    },
    0: {
        1: 'C началом трудовой деятельности в Банке России',
        2: 'Здравствуйте!\nЯ ассистент который поможет Вам адаптироваться на новом рабочем месте',
        3: "Пожалуйста, укажите, как к Вам можно обращаться:",
        4: 'Ваша адаптация начнется с первого рабочего дня.'
           '\nДля эффективной работы проверьте  включены ли уведомления в Телеграм',
        5: 'В ходе адаптации я буду Вам последовательно'
           '\nрекомендовать курсы и документы Банка России для изучения.'
           '\nИнформация о расположении курсов по команде /help',
        6: 'Ждем с нетерпением твоего выхода на работу.',
    },

    1: {
        1: "Доброе утро",
        2: "C первым рабочим днем в Банке России!",
        3: 'Сотрудники службы по работе с персоналом с нетерпением ждут тебя'
           '\nПозвоним им по телефону',
        4: 'Вы оформили все необходимые документы в подразделении по работе с персоналом?',
        5: 'Ваш руководитель готов пообщаться',
        6: 'Хотел узнать, как у тебя дела.'
           '\nГотов пройти небольшой чек-лист по первому дню?',

    },
    2: {
        1: 'Сегодня в рамках программы адаптации тебе необходимо пройти'
           '\nдистанционный курс <b>«Общение без ограничений»</b>',
        2: 'Осталось пройти, в рамках адаптации, последний но не менее важный курс'
           '\n<b>«Дистанционный курс и тестирование по САДД БР»</b>'
           '\nи обязательно выполнить тестирование по нему ',
        3: 'сегодня в рамках программы адаптации'
           '\nВам необходимо пройти вводный курс'
           '\n<b>"Добро пожаловать в Банк России"</b>',
        4: 'Вам необходимо пройти дистанционный курс\n'
           '<b>«Основы антикоррупции»</b>',
        5: 'Далее необходимо пройти дистанционный курс'
           '\n<b>«Обеспечение информационной безопасности при обработке '
           'информации ограниченного доступа в Банке России»</b>'
           '\nи тестирование по нему',

    }
}

QUESTIONS = {1: 'Рабочее место было организовано?',
             2: 'Почта подключена?',
             3: 'Удалось познакомиться с твоей командой?',
             4: 'Ты передал все документы для оформления в hr-службу?',
             5: 'Понятно ли, где можно пообедать?',
             6: 'Ты ознакомился с рабочим графиком?'
             }

QUEST_FIRST_LIST =['Рабочее место было организовано?',
                   'Почта подключена?',
                   'Удалось познакомиться с твоей командой?',
                   'Ты передал все документы для оформления в hr-службу?',
                   'Понятно ли, где можно пообедать?',
                   'Ты ознакомился с рабочим графиком?'
                   ]