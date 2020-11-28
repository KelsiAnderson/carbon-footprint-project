from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class EmissionTests(TestCase):
    """stuff to do before every test"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn()
