import logging

logger = logging.getLogger("masks")
file_handler = logging.FileHandler("../logs/masks.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_mask_card_number(card_number: int) -> str:
    """Функция маскировки номера карты"""
    logger.info("Маскируем номер карты")
    card = str(card_number)
    return f"{card[:4]} {card[4:6]}** **** {card[-4:]}"


def get_mask_account(mask_account: int) -> str:
    """Функция маскировки номера счета"""
    logger.info("Маскируем номер счета")
    numb = str(mask_account)
    return f"**{numb[-4:]}"
