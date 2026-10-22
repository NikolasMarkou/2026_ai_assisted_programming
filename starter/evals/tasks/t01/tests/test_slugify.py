import unittest

from slugify import slugify


class SlugifyTest(unittest.TestCase):
    def test_single_spaces(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_two_spaces(self):
        self.assertEqual(slugify("Hello  World"), "hello-world")
