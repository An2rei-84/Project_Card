import pandas as pd


def reading_csv_file(path):
    """������� ������ ������ �� ���� ������� .csv"""
    with open(path, encoding="utf-8") as file:
        reader = pd.read_csv(file, delimiter=';')
    return reader


def reading_exel_file(path):
    """������� ������ ������ �� ����� ������� .XLSX-"""
    wine_reviews = pd.read_excel(path)
    return wine_reviews


# print(reading_csv_file("../data/transactions.csv"))
# print(reading_exel_file("../data/transactions_excel.xlsx"))
