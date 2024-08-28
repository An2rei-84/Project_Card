import pandas as pd
import re
import logging

logger = logging.getLogger("services")
file_handler = logging.FileHandler("../logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def search_transactions(search_string):
    """Функция простого поиска из описания по вводимой строке"""
    df = pd.read_excel("../data/operations.xlsx")
    df = df.where(pd.notnull(df), "Неизвестно")

    list_search = df[df["Описание"].str.contains(search_string) | df["Категория"].str.contains(search_string)]
    logger.info("Функция search_transactions успешно отработала")
    return list_search.to_dict(orient="records")


# print(search_transactions('кино'))


def transfer_by_an_individual():
    """Функция поиска переводов физическим лицам"""
    df = pd.read_excel("../data/operations.xlsx")
    df = df.where(pd.notnull(df), "Неизвестно")
    logger.info("Создаем регулярное выражение дла функции transfer_by_an_individual")

    pattern = re.compile(
        "^[A-Я][а-яё]+\\s[А-Я]\\."
    )  # Регулярное выражение для поиска имени и первой буквы фамилии с точкой
    list_search = df[df["Категория"].str.contains("Переводы") & df["Описание"].str.match(pattern)]
    return list_search.to_dict(orient="records")


# print(transfer_by_an_individual())
