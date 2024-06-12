import masks


def mask_account_card(args: str) -> str:
    """Функция маскировки карты или счета"""
    data_account = str(args)
    new_number = int(args[-16:])
    if "Счет" in data_account:
        return f"Счет {masks.get_mask_account(new_number)}"
    else:
        data_card = data_account.replace(data_account[-16:], "")
        return f"{data_card[0:]}{masks.mask_card_number(new_number)}"


def get_data(args: str) -> str:
    """Функция определения даты"""
    data_ = str(args)
    return f"{data_[8:10]}.{data_[5:7]}.{data_[:4]}"
