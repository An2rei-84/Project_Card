from src.masks import mask_card_number, get_mask_account


my_list = 123456789123456


def tests_mask_card_number():
    assert mask_card_number(my_list) == "1234 56** **** 3456"


def tests_get_mask_account():
    assert get_mask_account(123456789) == "**6789"
