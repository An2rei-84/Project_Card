def filter_by_state(dicts_list: list, state="EXECUTED") -> list:
    """Функция возвращает новый список, содержащий только те словари,
    у которых ключ 'state'
    содержит переданное в функцию значение"""
    filtered_list = [i for i in dicts_list if i.get("state") == state]
    return filtered_list


def sort_by_date(transaction_info: list, is_date: bool = True) -> list:
    """Функция сортировки списка словарей по дате"""
    if is_date is True:
        return sorted(transaction_info, key=lambda x: x["date"], reverse=True)
    return sorted(transaction_info, key=lambda x: x["date"], reverse=False)
