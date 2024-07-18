import json
from unittest.mock import patch, mock_open
from src.utils import get_operations_list


def test_get_operations_list():
    mock_data = [{"code": "RUB"}]

    mock_file = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = get_operations_list("some_path")
        assert result == mock_data
