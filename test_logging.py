# import logging
#
# logger = logging.getLogger('logger')
#
# logger.setLevel('DEBUG')
# logger.setLevel(logging.DEBUG)
# logger.info('Делим на ноль')
# n = 0
# print(logger.level)
# logger.debug('debug info')
# logger.info('info')
# logger.warning('warning')
# logger.error('debug info')
# logger.critical('debug info')
# try:
#     rez = 1/n
# except :
#     logger.exception('ВНИМАНИЕ ОШИБКА!!!!!')
# else:
#     print(rez)

import sys
import logging
from logging import StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

logger.debug('debug information')