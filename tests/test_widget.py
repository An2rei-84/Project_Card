from src.widget import mask_account_card, get_data
import pytest

my_list_test_widget = "Visa Platinum 7000792289606361"
my_list_test_widget_2 = "Счет 73654108430135874305"


def test_widget_mask_account_card():
    assert mask_account_card(my_list_test_widget) == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card(my_list_test_widget_2) == "Счет **4305"


def test_widget_get_data():
    assert get_data("2018-07-11T02:26:18.671407") == "11.07.2018"


@pytest.mark.parametrize('string_, expected',
                         [('Visa Platinum 7000792289606361', 'Visa Platinum 7000 79** **** 6361'),
                          ('Счет 73654108430135874305', 'Счет **4305')
                          ])
def test_mask_account_card(string_, expected):
    assert mask_account_card(string_) == expected
