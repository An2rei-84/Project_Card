import unittest
from datetime import datetime
from unittest import mock
import pandas as pd
from src.utils import greeting, get_exchanges_rates, top_5_transactions, get_stock_prices
from unittest.mock import patch, Mock
import os
import json

class TestGreeting(unittest.TestCase):
    def test_greeting(self):
        now = datetime.now()
        result = greeting()
        expected = "Добрый вечер" if 22 > now.hour > 18 else "Добрый день" if 12 < now.hour < 18 \
            else "Доброе утро" if 6 < now.hour < 12 else "Доброй ночи"
        self.assertEqual(result, expected)


def test_get_exchanges_rates():
    # Создаем mock-объект для имитации ответа от API
    mock_response = mock.Mock()
    mock_response.json.return_value = [
        {"query": {"from": "USD", "to": "RUB", "amount": 1}, "info": {"rate": 70.0}},
        {"query": {"from": "EUR", "to": "RUB", "amount":1}, "info": {"rate": 65.0}}
    ]

    # Заменяем объект `requests.Session` на mock-объект
    with mock.patch('requests.Session.get', return_value=mock_response):
        # Вызываем функцию `get_exchanges_rates`
        exchanges_rates = get_exchanges_rates()

    # Проверяем, что функция вернула ожидаемый результат
    expected_result = [{'currency': 'USD', 'rate': 70.0}, {'currency': 'EUR', 'rate': 65.0}]
    assert len(exchanges_rates) == len(expected_result)
    for actual, expected in zip(exchanges_rates, expected_result):
        assert actual['currency'] == expected['currency']


class TestCalculateExpenses(unittest.TestCase):
    @patch('src.utils.calculate_expenses')
    def test_calculate_expenses(self, mock_calculate_expenses):
        # Создаем список транзакций
        transactions = [
            {"Номер карты": "1234567890123456", "Сумма операции": 100},
            {"Номер карты": "1234567890123456", "Сумма операции": -50},
            {"Номер карты": "1234567890123456", "Сумма операции": 200},
            {"Номер карты": "1234567890123456", "Сумма операции": -100},
            {"Номер карты": "1234567890123456", "Сумма операции": 300},
            {"Номер карты": "1234567890123456", "Сумма операции": -200},
            {"Номер карты": "1234567890123456", "Сумма операции": 400},
            {"Номер карты": "1234567890123456", "Сумма операции": -300},
        ]

        # Устанавливаем поведение мока
        mock_calculate_expenses.return_value = [
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
        ]

        # Вызываем функцию и проверяем результат
        expected_result = [
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
            {"last_digits": "1234", "total_spent": 100, "cashback": 2},
        ]
        result = mock_calculate_expenses(transactions)
        self.assertEqual(expected_result, result)


def test_top_5_transactions():

    df = pd.DataFrame({
        "Дата операции": ["2022-01-01", "2022-01-02", "2022-01-03"],
        "Сумма платежа": [100, 200, 300],
        "Категория": ["Расходы", "Доход", "Расходы"],
        "Описание": ["Оплата счета", "Продажа товара", "Покупка товара"]
    })

    # Проверяем, что функция возвращает список словарей
    result = top_5_transactions(df)
    assert isinstance(result, list)


class TestGetStockPrices(unittest.TestCase):
    @patch('requests.get')
    def test_get_stock_prices(self, mock_get):
        # Создание mock объекта для модуля requests
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'GLOBAL_QUOTE': {
                '05. price': 100.00
            }
        }
        mock_get.return_value = mock_response

        # Загрузка тестовых данных
        with open('user_settings.json', 'r') as file:
            data = json.load(file)

        # Замена API ключа на фиктивный
        os.environ['API_KEY_Alpha_Vantage2'] = 'MOCK_API_KEY'

        # Вызов функции get_stock_prices
        stock_prices = get_stock_prices()

        # Проверка, что функция вернула список с ценами акций
        self.assertIsInstance(stock_prices, list)
        self.assertEqual(len(stock_prices), len(data['user_stocks']))
        self.assertGreaterEqual(min(stock_prices, key=lambda x: x['price'])['price'], 0)

        # Удаление тестовой переменной окружения
        del os.environ['API_KEY_Alpha_Vantage2']


if __name__ == "__main__":
    unittest.main()