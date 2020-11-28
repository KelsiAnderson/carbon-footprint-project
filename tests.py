import unittest

from server import app
from model import db, connect_to_db

class EmissionTests(unittest.TestCase):
    """stuff to do before every test"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"logging in, logging in, logging in", result.data)

    def test_login(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>LOGIN</h2>', result.data)
        self.assertNotIn( b"<p>Don't have an account?</p>", result.data)

        print("DOES THIS WORK?")

    def test_new_account(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Don't have an account?</p>", result.data)
        self.assertNotIn(b"<h2>LOGIN</h2>", result.data)

        print("DO I WORK?")

if __name__ == "__main__":
    unittest.main()