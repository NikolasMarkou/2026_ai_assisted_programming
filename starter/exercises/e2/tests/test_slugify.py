import unittest

from slugify import slugify


class SlugifyTest(unittest.TestCase):
    def test_lowercases_and_joins_words_with_hyphens(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_drops_punctuation(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_repeated_separators_give_one_hyphen(self):
        self.assertEqual(slugify("a -- b   c___d"), "a-b-c-d")

    def test_no_hyphen_at_the_start_or_end(self):
        self.assertEqual(slugify("  --Title--  "), "title")

    def test_empty_string(self):
        self.assertEqual(slugify(""), "")

    def test_only_separators(self):
        self.assertEqual(slugify(" -- !! "), "")

    def test_accents_become_base_letters(self):
        self.assertEqual(slugify("Café Déjà Vu"), "cafe-deja-vu")

    def test_letters_without_an_ascii_form_are_dropped(self):
        self.assertEqual(slugify("日本語 2026"), "2026")

    def test_digits_are_kept(self):
        self.assertEqual(slugify("Release 3.12 notes"), "release-3-12-notes")

    def test_apostrophes_are_removed(self):
        self.assertEqual(slugify("Don't Stop"), "dont-stop")

    def test_curly_apostrophe_is_removed(self):
        self.assertEqual(slugify("Don’t Stop"), "dont-stop")


if __name__ == "__main__":
    unittest.main()
