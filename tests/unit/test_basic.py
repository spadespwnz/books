import unittest
from app import app
from fractions import Fraction
from sum import sum

class TestSum(unittest.TestCase):

    def setUp(self):

        self.app = app.test_client()
        self.app.testing = True

    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result,6)

    def test_list_fraction(self):
        """
        Test sums fractions
        """
        data = [Fraction(1,4), Fraction(1,4), Fraction(2,5)]
        result = sum(data)
        self.assertEqual(result,Fraction(9,10))

    def test_auto_pass(self):
        pass

    def test_code_error(self):
        with self.assertRaises(NameError):
            some_method()

    def test_home_status(self):
        result = self.app.get('/')

        self.assertEqual(result.status_code,200)
    def test_home_data(self):
        result = self.app.get('/')
        attrs = vars(result)

        self.assertGreater(len(result.data),0,"Page Length Should not be 0")

if __name__ == '__main__':
    unittest.main()
