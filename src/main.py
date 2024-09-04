import pandas as pd
from src.views import get_payments
from src.services import search_transactions, transfer_by_an_individual
from src.reports import spending_by_category


def main():
    print(get_payments("2021-12-25 05:12:10"))

    print(search_transactions("кино"))
    """Функция простого поиска из описания по вводимой строке"""

    print(transfer_by_an_individual())
    """Функция поиска переводов физическим лицам"""

    print(spending_by_category(list_transactions, "Авиабилеты", "28.04.2018"))
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Если дата не передана, то берется текущая дата."""


list_transactions = pd.read_excel("..\\data\\operations.xlsx")

# main()
