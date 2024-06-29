from src.generators import transaction_descriptions, filter_by_currency, card_number_generator


def test_transaction_descriptions(test_list_transaction):
    generator = transaction_descriptions(test_list_transaction)
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"


def test_filter_by_currency(test_list_transaction):
    generator = filter_by_currency(test_list_transaction, 'USD')
    generator_1 = filter_by_currency(test_list_transaction, 'RUB')
    assert next(generator)['id'] == 939719570
    assert next(generator)['id'] == 142264268
    assert next(generator_1)['id'] == 873106923


def test_card_number_generator():
    assert next(card_number_generator(1, 1)) == '0000 0000 0000 0001'
    assert next(card_number_generator(2, 2)) == '0000 0000 0000 0002'
    assert next(card_number_generator(3, 3)) != '0000 0000 0000 0005'
