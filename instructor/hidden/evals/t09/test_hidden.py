import unittest

from pairs import parse_pairs


class HiddenParsePairsTest(unittest.TestCase):
    def test_equals_in_the_middle(self):
        self.assertEqual(parse_pairs("q=a=b;n=1"), {"q": "a=b", "n": "1"})

    def test_trailing_semicolon(self):
        self.assertEqual(parse_pairs("a=1;"), {"a": "1"})

    def test_spaces_are_trimmed(self):
        self.assertEqual(parse_pairs(" a = 1 ; b = 2 "), {"a": "1", "b": "2"})

    def test_empty(self):
        self.assertEqual(parse_pairs(""), {})
