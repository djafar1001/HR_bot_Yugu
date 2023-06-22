from datetime import datetime


def format_time(timestamp: int) -> str:
    """
    Функция перевода времени из Unix формата
    :param timestamp: int: дата в формате Unix
    :return: df_time: str: строка с преобразованным форматом данных
    """
    dt_object = datetime.fromtimestamp(timestamp)
    df_time = f'{dt_object:%d-%m-%Y %H:%M:%S}'

    return df_time
