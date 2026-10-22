import unittest

from slugify import slugify


class HiddenSlugifyTest(unittest.TestCase):
    def test_many_spaces(self):
        self.assertEqual(slugify("a   b    c"), "a-b-c")

    def test_spaces_at_the_ends(self):
        self.assertEqual(slugify("  Hello World "), "hello-world")

    def test_tabs_and_newlines_separate_words(self):
        self.assertEqual(slugify("one\ttwo\nthree"), "one-two-three")

    def test_empty(self):
        self.assertEqual(slugify(""), "")
