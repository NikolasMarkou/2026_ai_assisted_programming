import unittest

from words import count_words


class CountWordsTest(unittest.TestCase):
    def test_plain_words(self):
        self.assertEqual(count_words("a b a"), {"a": 2, "b": 1})

    def test_punctuation(self):
        self.assertEqual(count_words("Hi, hi."), {"hi": 2})
