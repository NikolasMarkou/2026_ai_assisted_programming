import unittest

from words import count_words


class HiddenCountWordsTest(unittest.TestCase):
    def test_sentence(self):
        self.assertEqual(count_words("Hello, world! Hello."),
                         {"hello": 2, "world": 1})

    def test_question_and_dots(self):
        self.assertEqual(count_words("wait... what?"), {"wait": 1, "what": 1})

    def test_semicolon_and_colon(self):
        self.assertEqual(count_words("Stop; go: stop"), {"stop": 2, "go": 1})

    def test_empty(self):
        self.assertEqual(count_words(""), {})
