import unittest

from ranges import merge_ranges


class MergeRangesTest(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(merge_ranges([(1, 4), (3, 6)]), [(1, 6)])

    def test_touching(self):
        self.assertEqual(merge_ranges([(1, 3), (3, 5)]), [(1, 5)])
