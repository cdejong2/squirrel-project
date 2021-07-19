import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    ###############
    #### tests ####
    ###############

    def register(self, email, password):
        return self.app.post('/register',
                             data=dict(email=email,
                                       password=password,
                                       confirm_password=password),
                             follow_redirects=True)

    def test_valid_email_registration(self):
        response = self.register( 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)


    def test_invalid_email_registration(self):
        response = self.register('test@example', 'FlaskIsAwesome')
        self.assertIn(b'Not a valid email address.', response.data)
        response = self.register('testexample.com', 'FlaskIsAwesome')
        self.assertIn(b'Not a valid email address.', response.data)


if __name__ == "__main__":
    unittest.main()