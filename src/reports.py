import logging
from datetime import datetime, timedelta
import json
from functools import wraps
import pandas as pd

logger = logging.getLogger("reports")
file_handler = logging.FileHandler("../logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_to_file(filename=None):
    """Декоратор для записи результата функции в файл."""
    if filename is None:
        filename = "default_file.json"

    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(json.dumps(result, ensure_ascii=False))
            return result

        return wrapper

    return my_decorator


@log_to_file()
def spending_by_category(list_transactions, category, date: str = None):
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Если дата не передана, то берется текущая дата."""
    if date is None:
        date = datetime.now()
    else:
        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            logger.error("Некорректный формат даты.")

    three_months_ago = date - timedelta(days=90)
    three_months_ago = datetime.strftime(three_months_ago, "%d.%m.%Y")
    date = datetime.strftime(date, "%d.%m.%Y")
    list_transactions["Дата платежа"] = pd.to_datetime(list_transactions["Дата платежа"], dayfirst=True)
    filtered_transactions = list_transactions[
        (list_transactions["Категория"] == category)
        & (list_transactions["Дата платежа"] >= three_months_ago)
        & (list_transactions["Дата платежа"] <= date)
    ]

    total_spending_by_category = filtered_transactions.groupby(["Категория"])["Сумма платежа"].sum().reset_index()
    logger.info("Функция отработала.")
    return total_spending_by_category.to_dict(orient="records")


# list_transactions = pd.read_excel("..\\data\\operations.xlsx")
# print(spending_by_category(list_transactions, "Авиабилеты", "28.04.2018"))
