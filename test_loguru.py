# from loguru import logger
# a = 26
# b = 'Просто слово'
# c = [1, 2, 3]
#
# logger.add('./log/test_log.log', level='DEBUG')
#
#
#
#
#
# def testing_log(*args):
#     logger.debug(f'Просто выводит переменную a= {args[0]} и с= {args[2]}')
#     logger.info(f'Вывод информации о значении переменных\n'
#                 f'{" "*63}b = {args[1]}\n'
#                 f'{" "*63}c = {args[2]}')
#     if isinstance(b, int | str):
#         logger.warning(f'Предупреждение: b = {args[1]}')
#     else:
#         logger.error("b не является числом")
#     logger.error('Типа ошибка')
#     logger.critical('Остановка системы')
#
# @logger.catch(Exception, level=10, message='Произошла ошибка')
# def output_error(number: str):
#     while True:
#         try:
#             rez: int = int(number)
#         except ValueError:
#             logger.error(f'Введенное значение {number} не является числом')
#         else:
#             logger.info(f'Введено число {number}')
#             return rez ** 2
#
#
#
#
# testing_log(a, b, c)
# logger.info(f'Результат: {output_error(input("Введите число: "))}')
#
from loguru import logger

def debug_only(record):
    """
    Функция смены уровня логирования для использования ее в параметре filter=
    в методе add
    :param record:
    :return:
    """
    print(record)
    return record["level"].name == "DEBUG"

# Другие уровни отфильтровываются
logger.add("debug.log", filter=debug_only)