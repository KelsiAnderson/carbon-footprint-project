import unittest

from server import app
from model import db, example_data, connect_to_db #User, Vehicle, Vehicle_travel, Public_trans, Household, Monthly_Nat_Gas, Monthly_Elect 

class EmissionTests(unittest.TestCase):
    """stuff to do before every test"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b'Welcome', result.data)

        print("HI AM I WORKING?")

    def test_new_user_login(self):
        result = self.client.post("/new_users", data={"fname": "Susan", "password": "12345"}, follow_redirects=True)

        self.assertIn(b"You are a valued user", result.data)

        print("DOES THIS WORK?")

    def test_new_account(self):
        result = self.client.get("/existing_users")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Don't have an account?</p>", result.data)
        self.assertNotIn(b"<h2>LOGIN</h2>", result.data)

        print("DO I WORK?")

if __name__ == "__main__":
    import unittest
    
    unittest.main()