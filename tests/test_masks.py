from src.masks import get_mask_card_number, get_mask_account


my_list = 1234567891234567


def tests_mask_card_number():
    result = get_mask_card_number(my_list)
    assert result == "1234 56** **** 4567"
    assert len(result.replace(' ', '')) == 16


def tests_get_mask_account():
    assert get_mask_account(my_list) == "**4567"
