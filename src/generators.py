def filter_by_currency(transactions, currency):
    """Возвращает итератор операций с указанной валютой."""

    for operation in transactions:
        if operation["operationAmount"]["currency"]["code"] == currency:
            yield operation


def transaction_descriptions(transactions):
    """Принимает список словарей и возвращает описание каждой операции по очереди."""
    for i in transactions:
        yield i["description"]


def card_number_generator(start, stop):
    """Функция генерирует номера банковских карт"""
    for n in range(start, stop + 1):
        card_new_number = " ".join("{:016}".format(n)[i:i + 4] for i in range(0, 16, 4))
        yield card_new_number
