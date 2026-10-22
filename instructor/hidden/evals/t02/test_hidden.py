import unittest

from chunks import chunk


class HiddenChunkTest(unittest.TestCase):
    def test_size_larger_than_the_list(self):
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])

    def test_one_item_left_over(self):
        self.assertEqual(chunk(list("abcdefg"), 3),
                         [["a", "b", "c"], ["d", "e", "f"], ["g"]])

    def test_empty_list(self):
        self.assertEqual(chunk([], 3), [])

    def test_size_below_one_is_rejected(self):
        with self.assertRaises(ValueError):
            chunk([1], 0)
