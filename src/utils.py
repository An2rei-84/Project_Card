import json
import logging

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("../logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_operations_list(path):
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей
       с данными о финансовых транзакциях.
       Если файл пустой, содержит не список или не найден,
       функция возвращает пустой список."""
    logger.info("Формируем список словарей транзакций")
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.warning("Файл не найден")
        return []
    except json.JSONDecodeError:
        logger.warning("Ошибка в файле")
        return []
    if not isinstance(data, list):
        logger.warning("Файл не является списком")
        return []
    return data


# Пример использования функции
# operations_list = get_operations_list("../data/operations.json")
# print(operations_list)
