from unittest.mock import patch
from src.external_api import convert_transaction

transaction = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2020-12-03T18:35:29.512364",
    "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
}


@patch("requests.get")
def test_convert_transaction(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 4200.0}
    assert convert_transaction(transaction) == 4200.0


