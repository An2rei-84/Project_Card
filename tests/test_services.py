from unittest import mock

import pandas as pd
from src.services import search_transactions, transfer_by_an_individual


@mock.patch('pandas.read_excel')
def test_search_transactions(mock_read_excel):
    # Фиктивные данные для функции read_excel
    fake_data = pd.DataFrame({
        "Описание": ["строка 1", "строка 2"],
        "Категория": ["категория 1", "категория 2"]
    })
    mock_read_excel.return_value = fake_data

    # Вызов функции и проверка результата
    result = search_transactions("строка")
    assert len(result) == 2
    assert all([r['Описание'] == 'строка 1' or r['Описание'] == 'строка 2' for r in result])


@mock.patch('pandas.read_excel')
def test_transfer_by_an_individual(mock_read_excel):
    # Фиктивные данные для функции read_excel
    fake_data = pd.DataFrame({
        "Описание": ["Иванов И.", "Петров П."],
        "Категория": ["Переводы", "Переводы"]
    })
    mock_read_excel.return_value = fake_data

    # Вызов функции и проверка результата
    result = transfer_by_an_individual()
    assert len(result) == 2
    assert all([r['Описание'] == 'Иванов И.' or r['Описание'] == 'Петров П.' for r in result])
