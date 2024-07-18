import json


def get_operations_list(path):
    """Функция принимает на вход путь до JSON-файла и возвращает список словарей
       с данными о финансовых транзакциях.
       Если файл пустой, содержит не список или не найден,
       функция возвращает пустой список."""
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return data


# Пример использования функции
# operations_list = get_operations_list("../data/operations.json")
# print(operations_list)
