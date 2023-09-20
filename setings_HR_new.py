"""
Параметры для HR бота
"""

HR_BOT_TOKEN = {'name': '@Yugu_HR_bot',
                'URL': 'https://t.me/Yugu_HR_bot',
                'token': '6096922509:AAEVP8m7xiSLll0nZH7Z257siv4wasPxGEw'}

ADM_MESS = """
            Служебные слова для отладки:\n
            <b>удалить</b> - удаляет из памяти данные о пользователе чата\n
            <b>adm_sys</b> - высылает файл обо всех участниках чата
            """

# Сообщение для команды /help
HELP_MESSAGE = 'Курсы находятся на корпоративном портале,\n' \
            'в разделе "Карьера и развитие" выбираем "Учебный портал".\n' \
            'на странице портала выбираем "Дистанционное обучение"\n' \
            'и в поисковой строке указываем нужный курс'

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
        5: 'Вы успешно прошли все этапы адаптации\n'
           'Удачи в работе',
        6: 'Хорошо я вам напомню через час',
        7: 'Я настроен для начальной адаптации новых сотрудников\n'
           'К сожалению, я не могу Вам помочь в этом вопросе.😞',
        8: 'Выберите "да"  или "нет" в ответ на следующие вопросы',
        9: 'Спасибо  за прохождение опроса. Нам важно Ваше мнение.',
        10: 'Поздравляю Вас с первым рабочим днем!',
        11: 'Сегодня был важный и интересный день.\n '
            'Вы уже начали знакомиться с Банком России.\n '
            'Готовы поделиться впечатлениями о прожитом дне и пройденных курсах?',
        12: 'Введи ответ по 10-й шкале,\n '
            'где 0 - наименьший бал а 10 - наивысший'
    },
    0: {
        1: 'C началом трудовой деятельности в Банке России',
        2: 'Здравствуйте!\n'
           'Я ассистент который поможет Вам адаптироваться на новом рабочем месте',
        3: "Пожалуйста, укажите, как к Вам можно обращаться:",
        4: 'Ваша адаптация начнется с первого рабочего дня.\n'
           'Для эффективной работы проверьте  включены ли уведомления в Телеграм',
        5: 'В ходе адаптации я буду Вам последовательно\n'
           'рекомендовать курсы и документы Банка России для изучения.\n'
           'Информация о расположении курсов по команде /help',
        6: 'Ждем с нетерпением твоего выхода на работу.',
    },
    1: {
        1: "Доброе утро",
        2: "C первым рабочим днем в Банке России!",
        3: 'Сотрудники службы по работе с персоналом с нетерпением ждут тебя\n'
           'Позвони им по телефону',
        4: 'Вы оформили все необходимые документы в подразделении по работе с персоналом?',
        5: 'Ваш руководитель готов пообщаться\nЗайдите к нему',
        6: 'Хотел узнать, как у тебя дела.\n'
           'Готов пройти небольшой чек-лист по первому дню?',

    },
    2: {
        1: 'Сегодня в рамках программы адаптации\n'
           'Вам необходимо пройти вводный курс\n'
           '<b>"Добро пожаловать в Банк России"</b>',
        2: 'В рамках программы адаптации тебе необходимо изучить\n '
           '<b>ценности Банка России на корпоративном портале</b>',
        3: 'Далее необходимо изучить\n'
           '<b>стратегические цели Банка России и\n '
           'Карту Целей руководителя.</b>\n'
           'В этом тебе поможет непосредственный руководитель, обратись к нему.',
        4: 'Твой руководитель также может помочь изучить\n '
           '<b>модель компетенций Банка России.</b>',
        5: 'Вам необходимо пройти дистанционный курс\n'
           '<b>«Основы антикоррупции»</b>',
        6: 'Далее необходимо пройти дистанционный курс\n'
           '<b>«Обеспечение информационной безопасности при обработке '
           'информации ограниченного доступа в Банке России»</b>\n'
           'и тестирование по нему',
    },
    3: {
        7: 'Сегодня в рамках программы адаптации тебе необходимо пройти\n'
           'дистанционный курс <b>«Общение без ограничений»</b>',
        8: 'Осталось пройти, в рамках адаптации, последний но не менее важный курс\n'
           '<b>«Дистанционный курс и тестирование по САДД БР»</b>\n'
           'и обязательно выполнить тестирование по нему ',
        9: 'Сегодня в рамках программы адаптации тебе необходимо ознакомиться\n '
           '<b>с навигатором по риск-культуре  для вновь принятых работников'
           '(ПР-3-8-1-16/968 от 01.10.2021)</b>',
        10: 'В рамках программы адаптации тебе необходимо пройти дистанционный курс\n '
            '<b>«Основы управления рисками в Банке России»</b> и выполнить обязательное тестирование» ',
        11: 'В рамках программы адаптации тебе необходимо начать изучение\n'
            '<b><i>Федерального закона от 10.07.2002 № 86-ФЗ</i></b>\n'
            '<b>«О Центральном банке Российской Федерации (Банке России)»</b>.',
        12: 'Сегодня в рамках программы адаптации тебе необходимо начать изучение\n '
            '<b><i>Положения Банка России от 18.05.2015  № 468-П</i></b>\n'
            '<b>«Об обеспечении сохранности информации ограниченного доступа»</b>.',
        13: 'В рамках программы адаптации тебе необходимо начать изучение\n '
            '<b><i>Положения Банка России от 25.11.2015 № 506-П</i></b>\n'
            '<b>«Об обеспечении информационной безопасности\n'
            'в структурных подразделениях Банка России\n'
            'при обработке, хранении и (или) передаче информации\n'
            'с использованием средств вычислительной техники»</b>.',
        14: 'Сегодня в рамках программы адаптации тебе необходимо начать изучение\n '
            '<b><i>Положения Банка России от 11.04.2016 №538-П</i></b>\n '
            '<b>"О территориальных учреждениях"</b>.',
        15: 'В рамках программы адаптации тебе необходимо начать изучение\n'
            '<b><i>Инструкции Банка России от 29.12.2017 №186-И</i></b>\n '
            '<b>"О документационном обеспечении управления в учреждениях Банка России"</b>.',
    }
}

QUESTIONS = {1: 'Рабочее место было организовано?',
             2: 'Почта подключена?',
             3: 'Удалось познакомиться с твоей командой?',
             4: 'Ты передал все документы для оформления в hr-службу?',
             5: 'Понятно ли, где можно пообедать?',
             6: 'Ты ознакомился с рабочим графиком?'
             }

QUEST_FIRST_LIST = ['Рабочее место было организовано?',
                    'Почта подключена?',
                    'Удалось познакомиться с твоей командой?',
                    'Ты передал все документы для оформления в hr-службу?',
                    'Понятно ли, где можно пообедать?',
                    'Ты ознакомился с рабочим графиком?'
                    ]

QUEST_SECOND_LIST = ['Оцените удобство работы с чат ботом?',
                     'Оцените доступность и понятность материалов Банка России',
                     'Оцените собственный прогресс в достижении цели «Получение знаний о Банке России»'
                     ]

