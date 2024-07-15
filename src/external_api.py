import requests
import os
from dotenv import load_dotenv

load_dotenv("../.env")


def convert_transaction(transaction):
    """Эта функция конвертирует сумму транзакции в рубли."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency in ["USD", "EUR"]:
        api_key = os.getenv("API_KEY_CONVERT")
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": api_key},
            params={"from": currency, "to": "RUB", "amount": amount},
        )

        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                amount = data["result"]
            else:
                raise ValueError(f"Exchange rate for {currency} not found in API response")
        else:
            raise ConnectionError(f"status code: {response.status_code}")
    return amount

# Пример использования
# transaction = {
#     "id": 41428829,
#     "state": "EXECUTED",
#     "date": "2019-07-03T18:35:29.512364",
#     "operationAmount": {"amount": "8221", "currency": {"name": "USD", "code": "USD"}},
# }
#
# print(convert_transaction(transaction))
