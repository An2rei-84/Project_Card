import pandas as pd


def reading_csv_file(path):
    """The function returns a list of dictionaries from a csv file"""
    new_list = pd.read_csv(path, sep=";", header=0)
    return new_list.to_dict(orient="records")


def reading_exel_file(path):
    """The function returns a list of dictionaries from a xlsx file"""
    wine_reviews = pd.read_excel(path)
    return wine_reviews.to_dict(orient="records")


# print(reading_csv_file("../data/transactions.csv"))
# print(reading_exel_file("../data/transactions_excel.xlsx"))
