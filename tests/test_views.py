import unittest
import json
from src.views import get_payments


class TestGetPayments(unittest.TestCase):
    def test_returns_json(self):
        result = get_payments("2021-12-25 15:10:30")
        self.assertIsInstance(result, dict)
        self.assertTrue(isinstance(json.dumps(result), str))
