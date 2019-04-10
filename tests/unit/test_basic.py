import unittest
from app import create_app

from fractions import Fraction
from flask_pymongo import PyMongo
from sum import sum
from mockupdb import go, MockupDB, OpQuery

class TestOther(unittest.TestCase):
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

class TestDb(unittest.TestCase):
    def setUp(self):
        self.server = MockupDB(auto_ismaster={"maxWireVersion": 3})
        self.server.run()
        app = create_app("config_default.TestConfig",self.server.uri+"/test")
        self.app = app.test_client()



    def test_home_status(self):
        result = self.app.get('/')

        self.assertEqual(result.status_code,200)
    def test_home_data(self):
        result = self.app.get('/')
        attrs = vars(result)

        self.assertGreater(len(result.data),0,"Page Length Should not be 0")

    def test_api_home(self):

        future = go(self.app.get,"/api/")
        request = self.server.receives(OpQuery)
        request.reply({"test":"t"});
        http_response = future()
        print(http_response.get_data(as_text=True))
        self.assertIn(b"Api",http_response.get_data())


if __name__ == '__main__':
    unittest.main()
