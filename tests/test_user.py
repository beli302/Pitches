import unittest
from app.models import User
from os import urandom

class UserModelTest(unittest.TestCase):
    """
    Test class to test the behaviour of the user class
    """

    def setUp(self):
        """
        Set up method that will run before every Test
        """

        self.new_user = User(username='belinda', password = 'danette302')


    def test_password_setter(self):
        self.assertTrue(self.new_user.password_hash is not None)


    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password


    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('danette302'))



    def tearDown(self):
        user = User.query.filter_by(username="belinda").first()
        if user:
            print("found")
