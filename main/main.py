from src.processing import filter_by_state, sort_by_date
from src.reading import reading_csv_file, reading_exel_file
from src.search_end_sort import search_operations
from src.utils import get_operations_list
from src.widget import get_data, mask_account_card


def main():
    """Функция выводит список операций по выбранным фильтрам пользователя"""

    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
        Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла"""
    )

    select_list = []
    user_input = int(input())
    # В этом блоке определяем формат выбранного файла для обработки
    if user_input == 1:
        print("Для обработки выбран JSON-файл.")
        select_list = get_operations_list("../data/operations.json")

    elif user_input == 2:
        print("Для обработки выбран CSV-файл.")
        select_list = reading_csv_file("../data/transactions.csv")

    elif user_input == 3:
        print("Для обработки выбран XLSX-файл.")
        select_list = reading_exel_file("../data/transactions_excel.xlsx")

    else:
        print("Выбран не существующий пункт меню")

    while True:
        # В этом блоке определяется по какому статусу операций будем фильтровать
        print(
            """Введите статус, по которому необходимо выполнить фильтрацию. 
              Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"""
        )

        user_input_filter = input().upper()
        if user_input_filter == "CANCELED":
            print(f"Операции отфильтрованы по статусу {user_input_filter}")
            filtered_by_list = filter_by_state(select_list, user_input_filter)

            break
        elif user_input_filter == "EXECUTED":
            print(f"Операции отфильтрованы по статусу {user_input_filter}")
            filtered_by_list = filter_by_state(select_list, user_input_filter)
            break
        elif user_input_filter == "PENDING":
            print(f"Операции отфильтрованы по статусу {user_input_filter}")
            filtered_by_list = filter_by_state(select_list, user_input_filter)
            break
        else:
            print(f"Статус операции {user_input_filter} недоступен.")

    print("Отсортировать операции по дате? Да/Нет")
    user_ad_filter = input().lower()

    if user_ad_filter == "да":
        sort_by_date(filtered_by_list)

    print("Отсортировать по возрастанию или по убыванию?")
    user_ad_filter1 = input().lower()
    try:
        if user_ad_filter1 != "по возрастанию":
            filtered_by_list = sorted(filtered_by_list, key=lambda x: x["operationAmount"]["amount"], reverse=True)
        else:
            filtered_by_list = sorted(filtered_by_list, key=lambda x: x["operationAmount"]["amount"])
    except KeyError:
        if user_ad_filter1 != "по возрастанию":
            filtered_by_list = sorted(filtered_by_list, key=lambda x: x["amount"], reverse=True)
        else:
            filtered_by_list = sorted(filtered_by_list, key=lambda x: x["amount"])

    print("Выводить только рублевые транзакции? Да/Нет")
    user_ad_filter2 = input().upper()
    try:
        if user_ad_filter2 == "ДА":
            filtered_by_list = [x for x in filtered_by_list if x["operationAmount"]["currency"]["code"] == "RUB"]
    except KeyError:
        filtered_by_list = [x for x in filtered_by_list if x["currency_code"] == "RUB"]

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    user_ad_filter3 = input().upper()
    if user_ad_filter3 == "ДА":
        user_ad_filter4 = input("Введите ключевое слово:")

        filtered_by_list = search_operations(filtered_by_list, user_ad_filter4)

    count_key = lambda filtered_by_list, key: sum([1 for dictionary in filtered_by_list if key == "id" in dictionary])
    print("Распечатываю итоговый список транзакций...")
    result_key = count_key(filtered_by_list, "id")
    if filtered_by_list != []:

        print(f"Всего банковских операций в выборке: {result_key}")
    else:
        print("Не найдено ни одной транзакции,\n подходящей под ваши условия фильтрации")
    # Поскольку вложенность и названия ключей в разных форматах разная, то далее мучаемся с обработкой всего этого
    for i in filtered_by_list:
        # Если выбран json файл
        if user_input == 1:
            if i.get("description") != "Открытие вклада":
                data_list = get_data(i.get("date"))
                description_list = i.get("description")
                amount_list = i.get("operationAmount").get("amount")
                currency_list = i.get("operationAmount").get("currency").get("code")

                key_from = str(i.get("from", "0"))
                key_to = str(i.get("to"))
                from_list = mask_account_card(key_from)
                to_list = mask_account_card(key_to)
                print(
                    f"{data_list} {description_list}\n{from_list} -> {to_list}\nСумма {amount_list} {currency_list}\n"
                )

            if i.get("description") == "Открытие вклада":
                data_list = get_data(i.get("date"))
                description_list = i.get("description")
                amount_list = i.get("operationAmount").get("amount")
                currency_list = i.get("operationAmount").get("currency").get("code")
                key_to = str(i.get("to"))
                to_list = mask_account_card(key_to)

                print(f"{data_list} {description_list}\n{to_list}\nСумма {amount_list} {currency_list}\n")

        if user_input != 1:
            # Если выбран файл csv или xslx
            if i.get("description") != "Открытие вклада":
                data_list = get_data(i.get("date"))
                description_list = i.get("description")
                amount_list = i.get("amount")
                currency_list = i.get("currency_name")

                key_from = str(i.get("from", "0"))
                key_to = str(i.get("to"))
                from_list = mask_account_card(key_from)
                to_list = mask_account_card(key_to)
                print(
                    f"{data_list} {description_list}\n{from_list} -> {to_list}\nСумма {amount_list} {currency_list}\n"
                )

            if i.get("description") == "Открытие вклада":
                data_list = get_data(i.get("date"))
                description_list = i.get("description")
                amount_list = i.get("amount")
                currency_list = i.get("currency_name")
                key_to = str(i.get("to"))
                to_list = mask_account_card(key_to)

                print(f"{data_list} {description_list}\n{to_list}\nСумма {amount_list} {currency_list}\n")

    return filtered_by_list


starting = main()


