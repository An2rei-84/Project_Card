import datetime
import json
import pandas as pd
import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

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
# operations_list = get_operations_list("..\\data\\operations.json")
# print(operations_list)


def greeting():
    """Возвращает приветствие в зависимости от времени."""
    now = datetime.datetime.now()
    logger.info("Задаем параметры определения времени суток")
    if 6 < now.hour < 12:
        return "Доброе утро"
    elif 12 < now.hour < 18:
        return "Добрый день"
    elif 18 < now.hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# print(greeting())


def top_5_transactions(transactions_file):
    """Топ 5 транзакций по сумме платежа"""
    df = pd.DataFrame(transactions_file)
    list_transaction = df.sort_values(by="Сумма платежа").head()
    total_list = list_transaction.loc[:, ["Дата операции", "Сумма платежа", "Категория", "Описание"]]
    total_list.rename(columns={"Дата операции": "date", "Сумма платежа": "amount", "Категория": "category",
                               "Описание": "description"}, inplace=True)
    total_list["amount"] = total_list["amount"].apply(lambda x: abs(x))
    logger.info("Данные работы функции top_5_transactions сформированы")
    return total_list.to_dict(orient="records")


def calculate_expenses(transactions):
    """Рассчитывает общую сумму расходов и кешбэк по каждой карте."""
    total_amounts = {}
    cashback_amounts = {}
    cards = []
    for card in transactions:
        if (card["Номер карты"]) not in total_amounts:
            total_amounts[card["Номер карты"]] = abs(round(card["Сумма операции"], 2))
            cashback_amounts[card["Номер карты"]] = 0
        else:
            total_amounts[card["Номер карты"]] += abs(round(card["Сумма операции"]))
            current_cashback = cashback_amounts.get(card["Номер карты"])
            new_cashback = int(current_cashback + abs(card["Сумма операции"] / 100))
            cashback_amounts[card["Номер карты"]] = new_cashback

    for card_number, total_spent in total_amounts.items():
        last_digits = card_number[-4:]
        cashback = cashback_amounts.get(card_number, 0)
        cards.append({
            "last_digits": last_digits,
            "total_spent": total_spent,
            "cashback": cashback
        })
    for d in cards:
        d.update((k, "Неизвестная карта") for k, v in d.items() if v == "None")
        logger.info("Данные работы функции calculate_expenses сформированы")
    return cards


# print(calculate_expenses(reading_exel_file("..\\data\\operations.xlsx")))


def get_exchanges_rates():
    """Функция, которая возвращает курсы валют находящиеся в указанном файле"""
    dict_currency = []
    with open("user_settings.json", "r", encoding="utf-8") as file:
        date_user = json.load(file)
    api_key = os.getenv("API_KEY_CONVERT")
    logger.info("Формируем алгоритм запросов")
    for i in date_user["user_currencies"]:
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": api_key},
            params={"from": i, "to": "RUB", "amount": 1},
        )
        data = response.json()
        dict_currency.append(data)
    exchanges_rates = []
    for rate in dict_currency:
        exchanges_rates.append({
            "currency": rate['query']['from'],
            "rate": rate['info']['rate']
        })
        logger.info("Данные работы функции get_exchanges_rates сформированы")
    return exchanges_rates


# print(get_exchanges_rates())


def get_stock_prices():
    """Функция возвращает курсы акций указанных в файле"""
    logger.info("Запуск функции get_stock_prices")
    with open('user_settings.json', 'r') as file:
        data = json.load(file)
    api_key = os.getenv("API_KEY_Alpha_Vantage2")
    url = 'https://www.alphavantage.co/query?'
    params = {
        'function': 'GLOBAL_QUOTE',
        'outputsize': 'compact',
        'datatype': 'json',
        'apikey': api_key
    }

    stock_prices = []
    for symbol in data['user_stocks']:
        params['symbol'] = symbol
        response = requests.get(url, params=params)
        date = response.json()
        if response.status_code != 200:
            raise Exception(f"Ошибка при получении данных от API Alpha Vantage: {response.status_code}")
        price = date['GLOBAL_QUOTE']['05. price']
        stock_prices.append({
            "stock": symbol,
            "price": price
        })
    return stock_prices


# Пример использования функции
# stock_prices = get_stock_prices()
# print(get_stock_prices())
