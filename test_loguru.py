from loguru import logger
a = 26
b = 'Просто слово'
c = [1, 2, 3]

logger.add('./log/test_log.log', level='DEBUG')

def testing_log(*args):
    logger.debug(f'Просто выводит переменную a= {args[0]} и с= {args[2]}')
    logger.info(f'Вывод информации о значении переменных\n'
                f'{" "*63}b = {args[1]}\n'
                f'{" "*63}c = {args[2]}')
    logger.warning(f'Предупреждение: {args[1] if isinstance(b, int) else "b не является числом"} ')
    logger.error('Типа ошибка')
    logger.critical('Остановка системы')

@logger.catch(Exception, level=10, message='Произошла ошибка')
def output_error(number=None):
    try:
        number:int = int(input('Введите число: '))
    except ValueError:
        logger.error(f'Введенное значение {number} не является числом')
    else:
        logger.info(f'Введено число {number}')
        return number ** 2




#testing_log(a, b, c)
if output_error():
    logger.info(f'Результат: {output_error()}')

