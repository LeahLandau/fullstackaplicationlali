import unittest

from app import *


class TestYourApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Image-Reduction')

    def test_bad_request(self):
        response = self.app.get('/endpoint')
        self.assertEqual(response.status_code, 404)