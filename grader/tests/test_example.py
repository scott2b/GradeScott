import unittest
import submission


class TestExample(unittest.TestCase):

    def test_add(self):
        x, y = 1, 2
        expected = x + y
        result = submission.add(1, 2)
        self.assertEqual(expected, result, msg=f"Expected add({x}, {y}) == {expected}. Got: {result}")
