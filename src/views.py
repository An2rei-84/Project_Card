import datetime
import json
import pandas as pd
from src.utils import top_5_transactions, greeting, calculate_expenses, get_exchanges_rates, get_stock_prices
from dotenv import load_dotenv
import logging
load_dotenv("../.env")

logger = logging.getLogger("views")
file_handler = logging.FileHandler("../logs/views.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_payments(date: str):
    """Функция возвращающую JSON-ответ со следующими данными:
Приветствие в формате
По каждой карте:последние 4 цифры карты;общая сумма расходов;кешбэк (1 рубль на каждые 100 рублей).
Топ-5 транзакций по сумме платежа.
Курс валют. Стоимость акций из S&P500."""
    df = pd.read_excel("..\\data\\operations.xlsx")
    logger.info("Открываем файл")
    today_str = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    first_data = today_str.replace(day=1)
    first_data_str = first_data.strftime("%d.%m.%Y")
    end_data_str = today_str.strftime("%d.%m.%Y")
    # Преобразуем строки в объекты datetime.datetime
    first_data_obj = datetime.datetime.strptime(first_data_str, "%d.%m.%Y")
    end_data_obj = datetime.datetime.strptime(end_data_str, "%d.%m.%Y")
    # Преобразуем столбец с датами в датафрейме в объекты datetime
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    slice_date = df[(df["Дата операции"] >= first_data_obj) & (df["Дата операции"] <= end_data_obj)]
    slice_date = slice_date.where(pd.notnull(slice_date), "None")
    logger.info("Диапазон дат определен")
    slice_date["Дата операции"] = slice_date["Дата операции"].apply(
        lambda x: datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y"))

    slice_date_s = slice_date.to_dict(orient="records")

    information_user = dict()

    information_user["greeting"] = greeting()
    information_user["cards"] = calculate_expenses(slice_date_s)

    top_transactions = top_5_transactions(slice_date_s)
    information_user["top_transactions"] = top_transactions
    information_user["currency_rates"] = get_exchanges_rates()
    information_user["stock_prices"] = get_stock_prices()
    json.dumps(information_user)
    return information_user


# print(get_payments("2021-12-25 15:10:30"))
