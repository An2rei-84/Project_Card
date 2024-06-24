def get_mask_card_number(card_number: int) -> str:
    """Функция маскировки номера карты"""
    card = str(card_number)
    return f"{card[:4]} {card[4:6]}** **** {card[-4:]}"


def get_mask_account(mask_account: int) -> str:
    """Функция маскировки номера счета"""
    numb = str(mask_account)
    return f"**{numb[-4:]}"
