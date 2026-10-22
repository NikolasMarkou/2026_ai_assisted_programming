import unittest

from pairs import parse_pairs


class ParsePairsTest(unittest.TestCase):
    def test_two_pairs(self):
        self.assertEqual(parse_pairs("a=1;b=2"), {"a": "1", "b": "2"})

    def test_value_with_equals_signs(self):
        self.assertEqual(parse_pairs("token=abc=="), {"token": "abc=="})
