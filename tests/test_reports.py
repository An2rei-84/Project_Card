import json
from unittest.mock import patch
import pandas as pd
from unittest import mock
import pytest
from src.reports import spending_by_category, log_to_file
import os
import tempfile


@mock.patch('pandas.read_excel')
def test_spending_by_category(mock_read_excel):
    # Фиктивные данные для функции read_excel
    fake_data = pd.DataFrame({
        "Дата платежа": ["01.01.2022", "02.01.2022"],
        "Категория": ["Категория 1", "Категория 1"],
        "Сумма платежа": [100, 200]
    })
    mock_read_excel.return_value = fake_data
    # Тестовые данные для функции spending_by_category
    category = "Категория 1"
    date = "01.04.2022"
    # Вызов функции и проверка результата
    result = spending_by_category(fake_data, category, date)
    expected_result = [{"Категория": "Категория 1", "Сумма платежа": 300}]
    assert result == expected_result


def test_function():
    return {"result": "some data"}

@pytest.fixture
def mock_open(monkeypatch):
    with mock.patch('builtins.open', create=True) as mock_file:
        yield mock_file


def test_log_to_file(mock_open):
    decorated_function = log_to_file()(test_function)
    decorated_function()
    mock_open.assert_called_once_with("default_file.json", "w", encoding="utf-8")
