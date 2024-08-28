import pandas as pd


def reading_csv_file(path):
    """Функция принимает путь до файла и возвращает список словарей из файла csv"""
    new_list = pd.read_csv(path, sep=";", header=0)
    return new_list.to_dict(orient="records")


def reading_exel_file(path):
    """Функция принимает путь до файла и возвращает список словарей из файла xlsx"""
    wine_reviews = pd.read_excel(path)
    wine_reviews = wine_reviews.where(pd.notnull(wine_reviews), "None")
    return wine_reviews.to_dict(orient="records")


# print(reading_csv_file("..\\data\\transactions.csv"))
# print(reading_exel_file("..\\data\\transactions_excel.xlsx"))
