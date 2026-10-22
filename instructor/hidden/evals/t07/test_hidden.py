import unittest

from ranges import merge_ranges


class HiddenMergeRangesTest(unittest.TestCase):
    def test_chain_of_touching_ranges(self):
        self.assertEqual(merge_ranges([(5, 7), (1, 3), (3, 5)]), [(1, 7)])

    def test_gap_stays(self):
        self.assertEqual(merge_ranges([(1, 2), (4, 5)]), [(1, 2), (4, 5)])

    def test_contained_range(self):
        self.assertEqual(merge_ranges([(1, 10), (2, 3)]), [(1, 10)])

    def test_empty(self):
        self.assertEqual(merge_ranges([]), [])
