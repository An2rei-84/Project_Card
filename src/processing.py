def filter_by_state(dict_list: list, state="EXECUTED") -> list:
    """Функция возвращает новый список, содержащий только те словари,
    у которых ключ 'state'
    содержит переданное в функцию значение"""
    filtered_list = [i for i in dict_list if i.get("state") == state]
    return filtered_list


def sort_by_date(info: list, date=True) -> list:
    """Функция сортировки списка словарей по дате"""
    sorted_date = sorted(info, key=lambda x: x["date"], reverse=True)
    return sorted_date
