import unittest

from calc import average, spread


class Stats(unittest.TestCase):
    def test_average_of_whole_numbers(self):
        self.assertEqual(average([2, 4, 6]), 4)

    def test_average_keeps_the_fraction(self):
        self.assertEqual(average([1, 2]), 1.5)

    def test_spread(self):
        self.assertEqual(spread([3, 9, 5]), 6)


if __name__ == "__main__":
    unittest.main()
